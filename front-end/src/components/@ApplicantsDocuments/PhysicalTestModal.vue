<template>
  <el-dialog
    :visible="visible"
    :title="`Физическая подготовка: ${applicant ? applicant.fullname : ''}`"
    width="600px"
    @close="$emit('update:visible', false)"
  >
    <div v-loading="loading">
      <div
        v-for="(dirLabel, dir) in directions"
        :key="dir"
        class="direction-section"
      >
        <h3 class="direction-title">
          {{ dirLabel }}
        </h3>

        <div
          v-for="ex in addedExercises(dir)"
          :key="ex.exercise_type"
          class="exercise-row"
        >
          <span class="exercise-name">{{ ex.name }}</span>
          <!-- Ввод времени: MM мин SS сек -->
          <template v-if="ex.unit === 'мин'">
            <el-input-number
              :value="getMinutesPart(ex.exercise_type)"
              :min="0"
              :precision="0"
              :controls="false"
              size="small"
              class="exercise-input-time"
              @change="setMinutesPart(ex.exercise_type, $event)"
            />
            <span class="exercise-unit">мин</span>
            <el-input-number
              :value="getSecondsPart(ex.exercise_type)"
              :min="0"
              :max="59"
              :precision="0"
              :controls="false"
              size="small"
              class="exercise-input-time"
              @change="setSecondsPart(ex.exercise_type, $event)"
            />
            <span class="exercise-unit">сек</span>
          </template>
          <!-- Ввод секунд -->
          <template v-else-if="ex.unit === 'сек'">
            <el-input-number
              v-model="localResults[ex.exercise_type].value"
              :min="0"
              :controls="false"
              size="small"
              class="exercise-input"
              @input.native="handleDecimalInput($event, ex.exercise_type, 'value')"
            />
            <span class="exercise-unit">сек</span>
          </template>
          <!-- Ввод целых чисел (раз) -->
          <template v-else>
            <el-input-number
              v-model="localResults[ex.exercise_type].value"
              :min="0"
              :precision="0"
              :controls="false"
              size="small"
              class="exercise-input"
            />
            <span class="exercise-unit">{{ ex.unit || '' }}</span>
          </template>
          <template v-if="ex.extra_params && ex.extra_params.length">
            <span
              v-for="param in ex.extra_params"
              :key="param"
              class="extra-param"
            >
              <span class="extra-param-label">{{ extraParamLabel(param) }}</span>
              <el-input-number
                v-model="localResults[ex.exercise_type].extra_params[param]"
                :min="0"
                :controls="false"
                size="small"
                class="exercise-input"
                @input.native="handleDecimalInput($event, ex.exercise_type, 'extra_params', param)"
              />
            </span>
          </template>
          <el-button
            type="text"
            icon="el-icon-close"
            class="exercise-remove-btn"
            @click="removeExercise(ex.exercise_type)"
          />
        </div>

        <el-dropdown
          trigger="click"
          :disabled="remainingExercises(dir).length === 0"
          @command="addExercise"
        >
          <el-button type="text" size="small" icon="el-icon-plus">
            Добавить упражнение
          </el-button>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item
              v-for="ex in remainingExercises(dir)"
              :key="ex.exercise_type"
              :command="ex.exercise_type"
            >
              {{ ex.name }}
            </el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </div>
    </div>

    <span slot="footer">
      <el-button @click="$emit('update:visible', false)">Отмена</el-button>
      <el-button type="primary" :loading="loading" @click="save">Сохранить</el-button>
    </span>
  </el-dialog>
</template>

<script>
import {
  getExercises,
  getExerciseResults,
  createExerciseResult,
  updateExerciseResult,
  deleteExerciseResult,
} from "@/api/applicants";

const DIRECTIONS = {
  ST: "Сила",
  SP: "Быстрота",
  EN: "Выносливость",
};

export default {
  name: "PhysicalTestModal",

  props: {
    visible: {
      type: Boolean,
      default: false,
    },
    applicant: {
      type: Object,
      default: null,
    },
  },

  data() {
    return {
      directions: DIRECTIONS,
      exercisesByDirection: {},
      originalResults: {},
      localResults: {},
      loading: false,
    };
  },

  watch: {
    visible: {
      immediate: true,
      handler(val) {
        if (val) {
          this.loadData();
        }
      },
    },
  },

  methods: {
    async loadData() {
      if (!this.applicant) { return; }
      this.loading = true;
      try {
        const [exercisesResp, resultsResp] = await Promise.all([
          getExercises(),
          getExerciseResults(this.applicant.id),
        ]);

        // Group exercises by direction
        const byDirection = {};
        Object.keys(DIRECTIONS).forEach(dir => {
          byDirection[dir] = [];
        });
        exercisesResp.data.forEach(ex => {
          const dir = ex.direction || ex.dir;
          if (dir && byDirection[dir]) {
            byDirection[dir].push(ex);
          }
        });
        this.exercisesByDirection = byDirection;

        // Build results dictionary, ensuring all extra_params keys are initialized
        const allExercises = Object.values(byDirection).flat();
        const results = {};
        resultsResp.data.forEach(r => {
          const def = allExercises.find(e => e.exercise_type === r.exercise_type);
          const extraParamsInit = {};
          if (def && def.extra_params) {
            def.extra_params.forEach(param => {
              extraParamsInit[param] = (r.extra_params && r.extra_params[param] !== undefined)
                ? r.extra_params[param]
                : null;
            });
          }
          results[r.exercise_type] = {
            value: r.value,
            extra_params: Object.keys(extraParamsInit).length ? extraParamsInit : (r.extra_params || {}),
          };
        });
        this.originalResults = results;
        this.localResults = JSON.parse(JSON.stringify(results));
      } catch (e) {
        this.$message.error("Не удалось загрузить данные");
      } finally {
        this.loading = false;
      }
    },

    addedExercises(dir) {
      return (this.exercisesByDirection[dir] || []).filter(
        ex => ex.exercise_type in this.localResults,
      );
    },

    remainingExercises(dir) {
      return (this.exercisesByDirection[dir] || []).filter(
        ex => !(ex.exercise_type in this.localResults),
      );
    },

    addExercise(exerciseType) {
      const registry = this.exercisesByDirection;
      const extraParamsInit = {};
      Object.keys(registry).forEach(dir => {
        const ex = registry[dir].find(e => e.exercise_type === exerciseType);
        if (ex && ex.extra_params) {
          ex.extra_params.forEach(param => {
            extraParamsInit[param] = null;
          });
        }
      });
      this.$set(this.localResults, exerciseType, { value: 0, extra_params: extraParamsInit });
    },

    extraParamLabel(param) {
      const labels = {
        weight: "Вес, кг",
      };
      return labels[param] || param;
    },

    handleDecimalInput(event, exerciseType, field, paramName = null) {
      const input = event.target;
      if (!input) { return; }

      // Заменяем запятую на точку
      const originalValue = input.value;
      const normalizedValue = originalValue.replace(/,/g, ".");

      if (originalValue !== normalizedValue) {
        input.value = normalizedValue;

        // Trigger input event to update v-model
        const inputEvent = new Event("input", { bubbles: true });
        input.dispatchEvent(inputEvent);
      }
    },

    // --- Helpers for MM:SS input (unit === 'мин') ---

    getMinutesPart(exerciseType) {
      const value = this.localResults[exerciseType]
        ? (this.localResults[exerciseType].value || 0)
        : 0;
      return Math.floor(value);
    },

    getSecondsPart(exerciseType) {
      const value = this.localResults[exerciseType]
        ? (this.localResults[exerciseType].value || 0)
        : 0;
      return Math.round((value % 1) * 60);
    },

    setMinutesPart(exerciseType, minutes) {
      const seconds = this.getSecondsPart(exerciseType);
      const newValue = (minutes || 0) + (seconds || 0) / 60;
      this.$set(this.localResults[exerciseType], "value", Math.round(newValue * 100000) / 100000);
    },

    setSecondsPart(exerciseType, seconds) {
      const minutes = this.getMinutesPart(exerciseType);
      const newValue = (minutes || 0) + (seconds || 0) / 60;
      this.$set(this.localResults[exerciseType], "value", Math.round(newValue * 100000) / 100000);
    },

    removeExercise(exerciseType) {
      this.$delete(this.localResults, exerciseType);
    },

    findExerciseDefinition(exerciseType) {
      let foundExercise = null;
      Object.keys(this.exercisesByDirection).forEach(dir => {
        const ex = this.exercisesByDirection[dir].find(
          e => e.exercise_type === exerciseType,
        );
        if (ex) { foundExercise = ex; }
      });
      return foundExercise;
    },

    validateExtraParams() {
      let isValid = true;
      Object.entries(this.localResults).forEach(([type, result]) => {
        if (!isValid) { return; }
        const ex = this.findExerciseDefinition(type);
        if (ex && ex.extra_params && ex.extra_params.length > 0) {
          ex.extra_params.forEach(param => {
            if (!isValid) { return; }
            const value = result.extra_params?.[param];
            if (value === null || value === undefined || value === "") {
              this.$message.error(
                `Упражнение "${ex.name}": не указан параметр "${this.extraParamLabel(param)}"`,
              );
              isValid = false;
            } else if (typeof value === "number" && value <= 0) {
              this.$message.error(
                `Упражнение "${ex.name}": параметр "${this.extraParamLabel(param)}" должен быть больше нуля`,
              );
              isValid = false;
            }
          });
        }
      });
      return isValid;
    },

    async save() {
      // Валидация перед сохранением
      if (!this.validateExtraParams()) {
        return;
      }

      this.loading = true;
      try {
        // Удаления — последовательно, чтобы не конфликтовали транзакции и пересчёт баллов
        const deletePromises = Object.keys(this.originalResults)
          .filter(type => !(type in this.localResults))
          .map(type => deleteExerciseResult(this.applicant.id, type));

        // eslint-disable-next-line no-restricted-syntax
        for (const promise of deletePromises) {
          // eslint-disable-next-line no-await-in-loop
          await promise;
        }

        // Создания и обновления — параллельно
        const ops = [];
        Object.entries(this.localResults).forEach(([type, result]) => {
          if (type in this.originalResults) {
            const hasValueChanged = result.value !== this.originalResults[type].value;
            const hasParamsChanged = JSON.stringify(result.extra_params)
              !== JSON.stringify(this.originalResults[type].extra_params);

            if (hasValueChanged || hasParamsChanged) {
              ops.push(
                updateExerciseResult(this.applicant.id, type, {
                  value: result.value,
                  extra_params: result.extra_params,
                }),
              );
            }
          } else {
            ops.push(createExerciseResult(this.applicant.id, {
              exercise_type: type,
              value: result.value,
              extra_params: result.extra_params,
            }));
          }
        });
        await Promise.all(ops);

        this.$emit("saved");
        this.$emit("update:visible", false);
      } catch (e) {
        this.$message.error("Не удалось сохранить результаты");
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.direction-section {
  margin-bottom: 20px;
}

.direction-title {
  font-size: 14px;
  font-weight: bold;
  text-transform: uppercase;
  margin-bottom: 8px;
  color: #303133;
}

.exercise-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
  padding: 6px 10px;
  border: 1px solid #ebeef5;
  border-radius: 4px;
  background: #fafafa;
}

.exercise-name {
  flex: 1;
  font-size: 13px;
}

.exercise-input {
  width: 80px;
}

.exercise-input-time {
  width: 60px;
}

.exercise-unit {
  font-size: 12px;
  color: #909399;
  min-width: 30px;
}

.extra-param {
  display: flex;
  align-items: center;
  gap: 4px;
  margin-left: 8px;
  padding-left: 8px;
  border-left: 1px solid #dcdfe6;
}

.extra-param-label {
  font-size: 12px;
  color: #606266;
  white-space: nowrap;
}

.exercise-remove-btn {
  color: #f56c6c;
  padding: 0;
}
</style>
