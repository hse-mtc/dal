<template>
  <section class="formation-panel formation-remarks" aria-label="Замечания взводу">
    <div class="formation-panel-heading">
      <h3>Замечания <span class="formation-muted">{{ report ? report.remarks.length : "" }}</span></h3>
      <el-button
        v-if="report && canAdd"
        type="text"
        icon="el-icon-plus"
        :disabled="busy"
        @click="expanded = !expanded"
      >
        Добавить
      </el-button>
    </div>

    <div v-if="!report" class="formation-empty">
      <i class="el-icon-document" aria-hidden="true" />
      <strong>Сначала подайте сведения</strong>
      <p>После этого можно добавить замечания студентам.</p>
    </div>
    <template v-else>
      <article v-for="remark in report.remarks" :key="remark.id" class="formation-remark">
        <div class="formation-panel-heading">
          <strong>{{ remark.student_name }}</strong>
          <el-button
            v-if="canDelete"
            type="text"
            icon="el-icon-close"
            :disabled="busy"
            :aria-label="`Удалить замечание: ${remark.student_name}`"
            @click="$emit('remove', remark.id)"
          />
        </div>
        <span class="formation-category">{{ categoryLabel(remark.category) }}</span>
        <p v-if="remark.comment" class="formation-muted">
          {{ remark.comment }}
        </p>
      </article>
      <div v-if="!report.remarks.length && !expanded" class="formation-empty">
        <i class="el-icon-document-checked" aria-hidden="true" />
        <strong>Замечаний пока нет</strong>
        <p>Добавьте замечание при необходимости.</p>
      </div>

      <form v-if="expanded && canAdd" class="formation-remark-form" @submit.prevent="submit">
        <label class="formation-label" for="formation-student">Студент</label>
        <el-select
          id="formation-student"
          v-model="student"
          filterable
          :disabled="busy || studentsLoading"
          :loading="studentsLoading"
          placeholder="Начните вводить фамилию"
          no-data-text="Студенты не найдены"
        >
          <el-option
            v-for="person in students"
            :key="person.id"
            :label="person.fullname"
            :value="person.id"
          />
        </el-select>
        <div class="formation-label">
          Замечание
        </div>
        <div class="formation-categories" role="group" aria-label="Тип замечания">
          <button
            v-for="item in categories"
            :key="item.value"
            type="button"
            :aria-pressed="category === item.value"
            :disabled="busy"
            @click="category = item.value"
          >
            {{ item.label }}
          </button>
        </div>
        <label class="formation-label" for="formation-remark-comment">
          Пояснение <span class="formation-muted">· необязательно</span>
        </label>
        <el-input
          id="formation-remark-comment"
          v-model="comment"
          maxlength="255"
          :disabled="busy"
        />
        <div class="formation-remark-actions">
          <el-button
            native-type="submit"
            type="primary"
            :loading="busy"
            :disabled="!student || !category"
          >
            Добавить замечание
          </el-button>
          <el-button type="text" :disabled="busy" @click="expanded = false">
            Отмена
          </el-button>
        </div>
      </form>
      <p class="formation-meta">
        Замечания доступны начальнику цикла.
      </p>
    </template>
  </section>
</template>

<script>
export default {
  name: "FormationRemarks",
  props: {
    report: { type: Object, default: null },
    categories: { type: Array, required: true },
    students: { type: Array, required: true },
    studentsLoading: { type: Boolean, default: false },
    busy: { type: Boolean, default: false },
    canAdd: { type: Boolean, default: false },
    canDelete: { type: Boolean, default: false },
  },
  data() {
    return {
      expanded: false, student: null, category: null, comment: "",
    };
  },
  methods: {
    categoryLabel(value) {
      const category = this.categories.find(item => item.value === value);
      return category ? category.label : value;
    },
    submit() {
      if (this.student && this.category && !this.busy) {
        this.$emit("add", { student: this.student, category: this.category, comment: this.comment });
      }
    },
    reset() {
      this.expanded = false;
      this.student = null;
      this.category = null;
      this.comment = "";
    },
  },
};
</script>
