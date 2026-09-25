<template>
  <section class="formation-panel formation-headcount" :aria-label="`Численность взвода ${group.title}`">
    <div class="formation-panel-heading">
      <div>
        <span v-if="wizard" class="formation-muted">Шаг {{ step }} из 3</span>
        <h2 v-else>
          Взвод {{ group.title }}
        </h2>
        <p v-if="!wizard" class="formation-muted">
          Численность
        </p>
      </div>
      <span class="formation-status" :class="{ submitted: report }">
        {{ report ? "Сведения поданы" : "Нет сведений" }}
      </span>
    </div>

    <template v-if="wizard">
      <div class="formation-steps" aria-hidden="true">
        <span v-for="number in 3" :key="number" :class="{ active: step >= number }" />
      </div>
      <h2>{{ stepTitle }}</h2>
      <p class="formation-muted">
        Взвод {{ group.title }} · {{ formattedDate }}
      </p>
    </template>

    <fieldset :disabled="disabled || saving" class="formation-fields">
      <div v-if="!wizard || step < 3" class="formation-counts" :class="{ 'present-only': wizard && step === 2 }">
        <label v-if="!wizard || step === 1" class="formation-number">
          <span>По списку</span>
          <input
            :value="value.roster_count"
            :min="absentCount"
            max="9999"
            type="number"
            inputmode="numeric"
            step="1"
            aria-label="По списку"
            @input="setCount('roster_count', $event.target.value)"
          >
          <small v-if="!report && isHistoricalDate">Для прошлой даты проверьте численность</small>
        </label>
        <div class="formation-number present">
          <span>В строю</span>
          <output aria-label="В строю" aria-live="polite">{{ countsValid ? presentCount : "—" }}</output>
          <small>Рассчитывается автоматически</small>
        </div>
      </div>

      <div v-if="!wizard || step < 3" class="formation-all-present">
        <el-button type="text" :disabled="disabled || saving" @click="allPresent">
          Все в строю
        </el-button>
      </div>

      <div v-if="!wizard || step === 2" class="formation-reasons">
        <div class="formation-panel-heading">
          <h3>Отсутствуют</h3>
          <span class="formation-muted">{{ absentCount }} чел.</span>
        </div>
        <div v-for="reason in reasons" :key="reason.field" class="formation-reason">
          <label :for="`formation-${reason.field}`">{{ reason.label }}</label>
          <div class="formation-stepper">
            <button
              type="button"
              :disabled="disabled || saving || !(value[reason.field] > 0)"
              :aria-label="`Уменьшить: ${reason.label}`"
              @click="setCount(reason.field, value[reason.field] - 1)"
            >
              −
            </button>
            <input
              :id="`formation-${reason.field}`"
              :value="value[reason.field]"
              :max="reasonLimit(reason.field)"
              min="0"
              type="number"
              inputmode="numeric"
              step="1"
              :aria-label="reason.label"
              @input="setCount(reason.field, $event.target.value, $event.target)"
            >
            <button
              type="button"
              :disabled="disabled || saving || !countsValid || presentCount === 0"
              :aria-label="`Увеличить: ${reason.label}`"
              @click="setCount(reason.field, value[reason.field] + 1)"
            >
              +
            </button>
          </div>
        </div>
      </div>

      <dl v-if="wizard && step === 3" class="formation-recap">
        <div><dt>По списку</dt><dd>{{ value.roster_count }}</dd></div>
        <div><dt>В строю</dt><dd>{{ presentCount }}</dd></div>
        <div v-for="reason in reasons" :key="reason.field">
          <dt>{{ reason.label }}</dt><dd>{{ value[reason.field] }}</dd>
        </div>
      </dl>

      <p v-if="!countsValid && touched" class="formation-error" role="alert">
        {{ countError }}
      </p>

      <template v-if="!wizard || step === 3">
        <label class="formation-label" for="formation-comment">
          Комментарий <span class="formation-muted">· необязательно</span>
        </label>
        <el-input
          id="formation-comment"
          :value="value.comment"
          type="textarea"
          :rows="2"
          :disabled="disabled || saving"
          placeholder="Например, причину отсутствия уточняем"
          @input="update('comment', $event)"
        />
        <div class="formation-save">
          <span class="formation-muted" role="status">
            {{ !report ? "Сведения ещё не поданы" : dirty ? "Есть несохранённые изменения" : "Изменения сохранены" }}
          </span>
          <el-button
            type="primary"
            :loading="saving"
            :disabled="disabled || !countsValid || !dirty"
            @click="save"
          >
            {{ report ? "Сохранить изменения" : "Подать сведения" }}
          </el-button>
        </div>
      </template>
    </fieldset>

    <div v-if="wizard" class="formation-wizard-actions">
      <el-button v-if="step > 1" :disabled="saving" @click="step -= 1">
        Назад
      </el-button>
      <span v-else />
      <el-button
        v-if="step < 3"
        type="primary"
        :disabled="saving || !countsValid"
        @click="step += 1"
      >
        Продолжить <i class="el-icon-arrow-right" aria-hidden="true" />
      </el-button>
    </div>

    <p v-if="report" class="formation-meta">
      Подал: {{ report.created_by_email || "неизвестно" }}<br>
      Изменил: {{ report.updated_by_email || "неизвестно" }} · {{ updatedTime }}
    </p>
  </section>
</template>

<script>
import moment from "moment";

const reasons = [
  { field: "excused_count", label: "Уважительная причина" },
  { field: "unexcused_count", label: "Неуважительная причина" },
  { field: "unknown_count", label: "Причина не выяснена" },
];
const fields = ["roster_count", ...reasons.map(reason => reason.field)];

export default {
  name: "FormationHeadcount",
  props: {
    value: { type: Object, required: true },
    group: { type: Object, required: true },
    report: { type: Object, default: null },
    date: { type: String, required: true },
    wizard: { type: Boolean, default: false },
    saving: { type: Boolean, default: false },
    disabled: { type: Boolean, default: false },
  },
  data() {
    return { reasons, step: 1, touched: false };
  },
  computed: {
    isHistoricalDate() {
      return this.date < moment().format("YYYY-MM-DD");
    },
    absentCount() {
      return reasons.reduce((sum, reason) => sum + (this.value[reason.field] || 0), 0);
    },
    presentCount() {
      return this.value.roster_count - this.absentCount;
    },
    countsValid() {
      return fields.every(field => Number.isInteger(this.value[field])
        && this.value[field] >= 0 && this.value[field] <= 9999) && this.presentCount >= 0;
    },
    countError() {
      return this.presentCount < 0
        ? `По списку должно быть не меньше ${this.absentCount} — столько уже отмечено отсутствующими.`
        : "Введите целые числа от 0 до 9999.";
    },
    dirty() {
      return !this.report || [...fields, "comment"].some(field => this.value[field] !== this.report[field]);
    },
    stepTitle() {
      return ["Сколько человек по списку?", "Почему отсутствуют?", "Проверьте сведения"][this.step - 1];
    },
    formattedDate() {
      return moment(this.date).format("DD.MM.YYYY");
    },
    updatedTime() {
      return moment(this.report.updated_at).format("DD.MM.YYYY HH:mm");
    },
  },
  methods: {
    update(field, value) {
      this.$emit("input", { ...this.value, [field]: value });
    },
    reasonLimit(field) {
      const otherAbsent = reasons.filter(reason => reason.field !== field)
        .reduce((sum, reason) => sum + (this.value[reason.field] || 0), 0);
      return Math.max(0, (this.value.roster_count || 0) - otherAbsent);
    },
    setCount(field, raw, input) {
      this.touched = true;
      let value = raw === "" ? null : Number(raw);
      if (field !== "roster_count" && Number.isInteger(value)) {
        value = Math.max(0, Math.min(this.reasonLimit(field), value));
        if (input && Number(raw) !== value) {
          Object.assign(input, { value });
        }
      }
      this.update(field, value);
    },
    allPresent() {
      this.$emit("input", {
        ...this.value, excused_count: 0, unexcused_count: 0, unknown_count: 0,
      });
    },
    save() {
      if (this.countsValid && this.dirty && !this.disabled && !this.saving) {
        this.$emit("save", { ...this.value, present_count: this.presentCount });
      }
    },
  },
};
</script>
