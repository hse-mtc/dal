<template>
  <PrimeTable
    ref="primeTable"
    :value="data"
    class="p-datatable-gridlines"
    frozen-width="400px"
    :row-hover="true"
    auto-layout
    scrollable
    edit-mode="cell"
    scroll-height="60vh"
    @cell-edit-init="savePrevValue"
  >
    <PrimeColumn
      v-for="({ abbr, title, width, rotate = true }, field) in fields"
      :key="field"
      :column-key="field"
      :field="data => getCellText(data, field)"
      :header-style="
        rotate
          ? `height: 200px; width: ${width}px; writing-mode: vertical-rl; transform: rotate(180deg); text-align: right`
          : `height: 200px; width: ${width}px`
      "
      :body-style="`width: ${width}px; height: 110px`"
      :body-class="cellBodyClass(field)"
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

      <template
        v-if="field === 'index'"
        #body="{ index }"
      >
        <a
          title="Зарегистрировать в качестве студента ВУЦа"
          style="cursor: pointer; text-decoration: default; color: black;"
          @click="navigateToApplicantToStudent(data[index])"
        >
          {{ startIndex + index + 1 }}
        </a>
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

        <NumberInput
          v-if="field === 'pull_ups'"
          v-model="editorData[field]"
          :controls="false"
          :min="0"
          :min-fraction-digits="0"
          :max-fraction-digits="0"
          @change="onUpdate(editorData, field, $event || 0)"
        />

        <NumberInput
          v-if="field === 'speed_run'"
          v-model="editorData[field]"
          :controls="false"
          :min="0"
          :min-fraction-digits="1"
          :max-fraction-digits="1"
          @change="onUpdate(editorData, field, $event || 0)"
        />

        <NumberInput
          v-if="field === 'long_run'"
          v-model="editorData[field]"
          :controls="false"
          :min="0"
          :min-fraction-digits="1"
          :max-fraction-digits="1"
          @change="onUpdate(editorData, field, $event || 0)"
        />

        <NumberInput
          v-if="field === 'physical_test_grade'"
          v-model="editorData[field]"
          :controls="false"
          :max="100"
          :min="0"
          :min-fraction-digits="0"
          :max-fraction-digits="0"
          @change="onUpdate(editorData, field, $event || 0)"
        />
      </template>
    </PrimeColumn>
  </PrimeTable>
</template>

<script>
import {
  Component, Prop, Vue, Watch,
} from "vue-property-decorator";
import { SelectInput, SingleCheckbox, NumberInput } from "@/common/inputs";
import { UserModule } from "@/store";

const fields = {
  index: {
    title: "№",
    width: 50,
    rotate: false,
  },
  fullname: {
    abbr: "Фамилия, имя, отчество",
    title: "Фамилия, имя, отчество",
    width: 300,
    rotate: false,
  },
  birthday: {
    title: "Дата рождения",
    width: 120,
    rotate: false,
  },
  faculty: {
    abbr: "Факультет",
    title: "Факультет",
    width: 250,
    rotate: false,
  },
  program: {
    abbr: "Код специальности (направление подготовки)",
    title: "Код специальности (направление подготовки)",
    width: 250,
    rotate: false,
  },
  mean_grade: {
    title: "Средний балл",
    width: 100,
    rotate: false,
  },
};

const additionalFields = {
  medical_examination: {
    abbr: "Результаты медицинского освидетельствования",
    title: "Результаты медицинского освидетельствования",
    width: 200,
    rotate: false,
  },
  prof_psy_selection: {
    abbr: "Результаты профессионального психологического отбора",
    title: "Результаты профессионального психологического отбора",
    width: 100,
  },
  preferential_right: {
    abbr: "Преимущественное право",
    title: "Преимущественное право",
    width: 100,
  },
  characteristic_handed_over: {
    abbr: "Характеристика",
    title: "Характеристика",
    width: 100,
  },
  criminal_record_handed_over: {
    abbr: "Справка о несудимости",
    title: "Справка о несудимости",
    width: 100,
  },
  passport_handed_over: {
    title: "Паспорт",
    width: 100,
  },
  registration_certificate_handed_over: {
    abbr: "Приписное свидетельство",
    title: "Приписное свидетельство",
    width: 100,
  },
  university_card_handed_over: {
    abbr: "Студенческий билет",
    title: "Студенческий билет",
    width: 100,
  },
  application_handed_over: {
    title: "Заявление",
    width: 120,
  },
  pull_ups: {
    title: "Сила",
    width: 140,
  },
  speed_run: {
    title: "Скорость",
    width: 100,
  },
  long_run: {
    title: "Выносливость",
    width: 100,
  },
  physical_test_grade: {
    abbr: "ФИЗО",
    title: "Итоговая оценка за физические испытания",
    width: 100,
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

  fields = UserModule.email.includes("study.office")
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
    "pull_ups",
    "speed_run",
    "long_run",
    "physical_test_grade",
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
    this.currentEditingValue = data[field];
  }

  synchronizeHeights() {
    this.$nextTick(() => {
      const rowsFrozen = this.$refs.primeTable.$el.querySelectorAll(".p-datatable-frozen-view tr");
      const rowsUnfrozen = this.$refs.primeTable.$el.querySelectorAll(".p-datatable-unfrozen-view tr");
      if (rowsFrozen.length !== rowsUnfrozen.length) {
        console.error("Mismatch in row count between frozen and scrollable sections");
        return;
      }

      for (let i = 0; i < rowsFrozen.length; i += 1) {
        const frozenRow = rowsFrozen[i];
        const scrollableRow = rowsUnfrozen[i];

        const frozenHeight = frozenRow.offsetHeight;
        const scrollableHeight = scrollableRow.offsetHeight;
        const maxHeight = Math.max(frozenHeight, scrollableHeight);

        frozenRow.style.height = `${maxHeight}px`;
        scrollableRow.style.height = `${maxHeight}px`;
      }
    });
  }

  cellBodyClass(field) {
    const arr = [];
    if (this.editableFields.includes(field)) {
      arr.push(this.$style.editableField);
    }
    if (["index", "fullname"].includes(field)) {
      arr.push("frozen-cell");
    } else {
      arr.push("scrollable-cell");
    }
    return arr.join(" ");
  }

  mounted() {
    this.synchronizeHeights();
  }

  @Watch("data", { immediate: true, deep: true })
  onDataChanged(newVal, oldVal) {
    this.synchronizeHeights();
  }

  getCellText(data, field) {
    const getSelectLabel = (value, options) => {
      const option = options.find(item => item.value === value);

      if (option) { return option.label; }

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
      if (data[field] === undefined) {
        return "---";
      }
      return (+data[field]).toFixed(2);
    }

    if (field === "pull_ups") {
      if (data[field] === undefined) {
        return "---";
      }
      return +data[field];
    }

    if (field === "speed_run") {
      if (data[field] === undefined) {
        return "---";
      }
      return (+data[field]).toFixed(2);
    }

    if (field === "long_run") {
      if (data[field] === undefined) {
        return "---";
      }
      return (+data[field]).toFixed(2);
    }

    if (field === "physical_test_grade") {
      if (data[field] === undefined) {
        return 0;
      }
      return +data[field];
    }

    return data[field];
  }

  navigateToApplicantToStudent(data) {
    this.$router.push({ name: "ApplicantToStudent", query: { userId: data.id } });
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
