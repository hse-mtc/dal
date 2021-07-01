<template>
  <PrimeTable
    :value="data"
    class="p-datatable-gridlines p-datatable-striped"
    frozen-width="400px"
    auto-layout
    scrollable
    edit-mode="cell"
    scroll-height="60vh"
    @cell-edit-init="savePrevValue"
  >
    <PrimeColumn
      v-for="({ abbr, title, width }, field) in fields"
      :key="field"
      :column-key="field"
      :field="data => getCellText(data, field)"
      :header-style="`width: ${width}px; height: 120px`"
      :body-style="`width: ${width}px; height: 110px`"
      :body-class="editableFields.includes(field) ? $style.editableField : ''"
      :frozen="['index', 'fullname'].includes(field)"
    >
      <template #header>
        <div>
          <el-popover
            v-if="abbr"
            placement="top-start"
            trigger="hover"
            :content="title"
          >
            <span slot="reference">{{ abbr }}</span>
          </el-popover>
          <span v-else>{{ title }}</span>
        </div>
      </template>

      <template #body="{ data: row, index: $index }">
        <template v-if="field === 'index'">
          {{ startIndex + $index + 1 }}
        </template>

        <template v-else-if="field === 'medical_examination'">
          {{ row[field] | getSelectLabel(medicalExaminationOptions) }}
        </template>

        <template v-else-if="field === 'prof_psy_selection'">
          {{ row[field] | getSelectLabel(profPsySelection) }}
        </template>

        <template v-else-if="checkboxesFields.includes(field)">
          {{ row[field] ? 'Есть' : 'Нет' }}
        </template>

        <template v-else-if="field === 'mean_grade'">
          {{ (+row[field]).toFixed(2) }}
        </template>

        <template v-else>
          {{ row[field] }}
        </template>
      </template>

      <template
        v-if="editableFields.includes(field)"
        #editor="{ data: editorData }"
      >
        <SelectInput
          v-if="field === 'medical_examination'"
          v-model="editorData[field]"
          :options="medicalExaminationOptions"
          :clearable="true"
          @change="onUpdate(editorData, field, $event)"
        />

        <SelectInput
          v-if="field === 'prof_psy_selection'"
          v-model="editorData[field]"
          :options="profPsySelection"
          :clearable="true"
          @change="onUpdate(editorData, field, $event)"
        />

        <SingleCheckbox
          v-if="checkboxesFields.includes(field)"
          v-model="editorData[field]"
          :checkbox-label="editorData[field] ? 'Есть' : 'Нет'"
          @change="onUpdate(editorData, field, $event)"
        />

        <NumberInput
          v-if="field === 'mean_grade'"
          v-model="editorData[field]"
          :controls="false"
          :max="10"
          :min="0"
          :min-fraction-digits="2"
          :max-fraction-digits="2"
          @change="onUpdate(editorData, field, $event || 0)"
        />
      </template>
    </PrimeColumn>
  </PrimeTable>
</template>

<script>
import { Component, Prop, Vue } from "vue-property-decorator";
import { SelectInput, SingleCheckbox, NumberInput } from "@/common/inputs";

const fields = {
  index: {
    title: "№",
    width: 50,
  },
  fullname: {
    abbr: "ФИО",
    title: "Фамилия, имя, отчество",
    width: 300,
  },
  birthday: {
    title: "Дата рождения",
    width: 120,
  },
  program: {
    abbr: "КС",
    title: "Код специальности (направление подготовки)",
    width: 100,
  },
  mean_grade: {
    title: "Средний балл",
    width: 100,
  },
};

const additionalFields = {
  medical_examination: {
    abbr: "РМО",
    title: "Результаты медицинского освидетельствования",
    width: 200,
  },
  prof_psy_selection: {
    abbr: "РППО",
    title: "Результаты профессионального психологического отбора",
    width: 100,
  },
  preferential_right: {
    abbr: "ПП",
    title: "Преимущественное право",
    width: 100,
  },
  characteristic_handed_over: {
    abbr: "Хар-ка",
    title: "Характеристика",
    width: 100,
  },
  criminal_record_handed_over: {
    abbr: "СН",
    title: "Справка о несудимости",
    width: 100,
  },
  passport_handed_over: { title: "Паспорт", width: 100 },
  registration_certificate_handed_over: {
    abbr: "ПС",
    title: "Приписное свидетельство",
    width: 100,
  },
  university_card_handed_over: {
    abbr: "СБ",
    title: "Студенческий билет",
    width: 100,
  },
  application_handed_over: {
    title: "Заявление",
    width: 120,
  },
};

const medicalExaminationOptions = [
  { label: "Годен", value: "FI" },
  { label: "Годен с незначительными ограничениями", value: "FMR" },
  { label: "Ограниченно годен", value: "FLI" },
  { label: "Ограниченно не годен", value: "UR" },
  { label: "Не годен", value: "UN" },
];

const profPsySelection = [
  { label: "I", value: "FI" },
  { label: "II", value: "SE" },
  { label: "III", value: "TH" },
  { label: "IV", value: "FO" },
];

const checkboxesFields = [
  "preferential_right",
  "characteristic_handed_over",
  "criminal_record_handed_over",
  "passport_handed_over",
  "registration_certificate_handed_over",
  "university_card_handed_over",
  "application_handed_over",
];

@Component({
  name: "ApplicantsDocuments",
  components: {
    SelectInput,
    SingleCheckbox,
    NumberInput,
  },
})
class ApplicantsDocuments extends Vue {
  @Prop({ type: Array, required: true, default: () => [] }) data
  @Prop({ type: Number, required: true }) startIndex
  @Prop({ type: Function, default: () => true }) onChange

  // undefined, so as not to be reactive
  currentEditingValue = undefined

  fields = this.$store.state.user.email.includes("study.office")
    ? fields
    : {
      ...fields,
      ...additionalFields,
    }

  checkboxesFields = checkboxesFields
  editableFields = [
    ...checkboxesFields,
    "mean_grade",
    "medical_examination",
    "prof_psy_selection",
  ]

  medicalExaminationOptions = medicalExaminationOptions
  profPsySelection = profPsySelection

  async onUpdate(data, key, value) {
    if (!await this.onChange({ id: data.id, key, value })) {
      // eslint-disable-next-line no-param-reassign
      data[key] = this.currentEditingValue;
    } else {
      this.currentEditingValue = value;
    }
  }

  savePrevValue({ data, field }) {
    console.log("field", field);
    this.currentEditingValue = data[field];
  }

  getCellText(data, field) {
    const getSelectLabel = (value, options) => {
      const option = options.find(item => item.value === value);

      if (option) return option.label;

      return "Выбрать";
    };

    if (field === "medical_examination") {
      return getSelectLabel(data[field], medicalExaminationOptions);
    }

    if (field === "prof_psy_selection") {
      return getSelectLabel(data[field], profPsySelection);
    }

    if (checkboxesFields.includes(field)) {
      return data[field] ? "Есть" : "Нет";
    }

    if (field === "mean_grade") {
      return (+data[field]).toFixed(2);
    }

    return data[field];
  }
}

export default ApplicantsDocuments;
</script>

<style lang="scss" module>
@import "@/styles/variables.scss";

.label {
  word-break: break-word !important;
}

.editableField {
  cursor: pointer;

  &:hover {
    color: $darkBlue;
  }
}

// hide number input controls
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance: none;
}
input[type="number"]{
  -moz-appearance: textfield;
}
</style>
