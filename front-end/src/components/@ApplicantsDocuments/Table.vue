<template>
  <el-table :data="data" border>
    <el-table-column
      v-for="({ abbr, title, width }, field) in fields"
      :key="field"
      :prop="field"
      :label="title"
      :width="width"
      :fixed="['index', 'fullname'].includes(field)"
      :label-class-name="$style.label"
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

      <template slot-scope="{ row, $index }">
        <template v-if="field === 'index'">
          <span>{{ startIndex + $index + 1 }}</span>
        </template>

        <template v-else-if="field === 'mean_grade'">
          <!-- todo -->
          <!-- eslint-disable vue/no-mutating-props -->
          <el-input
            v-model="data[$index][field]"
            style="width: 100%; max-width: 100%"
            type="number"
            :controls="false"
            @blur="checkGrade(row.id, field, $index, field)"
          />
          <!-- eslint-enable vue/no-mutating-props -->
        </template>

        <template v-else-if="field === 'medical_examination'">
          <!-- todo -->
          <!-- eslint-disable vue/no-mutating-props -->
          <SelectInput
            v-model="data[$index][field]"
            :options="[
              { label: 'Годен', value: 'FI' },
              { label: 'Годен с незначительными ограничениями', value: 'FMR' },
              { label: 'Ограниченно годен', value: 'FLI' },
              { label: 'Ограниченно не годен', value: 'UR' },
              { label: 'Не годен', value: 'UN' },
            ]"
            :clearable="true"
            @change="onUpdate(row.id, field, $event)"
          />
          <!-- eslint-enable vue/no-mutating-props -->
        </template>

        <template v-else-if="field === 'prof_psy_selection'">
          <!-- todo -->
          <!-- eslint-disable vue/no-mutating-props -->
          <SelectInput
            v-model="data[$index][field]"
            :options="[
              { label: 'I', value: 'FI' },
              { label: 'II', value: 'SE' },
              { label: 'III', value: 'TH' },
              { label: 'IV', value: 'FO' },
            ]"
            :clearable="true"
            @change="onUpdate(row.id, field, $event)"
          />
          <!-- eslint-enable vue/no-mutating-props -->
        </template>

        <template v-else-if="checkboxesFields.includes(field)">
          <!-- todo -->
          <!-- eslint-disable vue/no-mutating-props -->
          <SingleCheckbox
            v-model="data[$index][field]"
            checkbox-label="Есть"
            @change="onUpdate(row.id, field, $event)"
          />
          <!-- eslint-enable vue/no-mutating-props -->
        </template>

        <template v-else>
          {{ row[field] }}
        </template>
      </template>
    </el-table-column>
  </el-table>
</template>

<script>
import { SelectInput, SingleCheckbox } from "@/common/inputs";

export default {
  name: "ApplicantsDocuments",
  components: {
    SelectInput,
    SingleCheckbox,
  },
  props: {
    data: {
      required: true,
      type: Array,
      default: () => [],
    },
    startIndex: {
      required: true,
      type: Number,
    },
  },
  data() {
    // TODO(gakhromov): remove this check when permissions are done
    const userEmail = this.$store.state.user.email;
    let fields = {
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
        width: 100,
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

    if (!userEmail.includes("study.office")) {
      fields = {
        ...fields,
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
          width: 100,
        },
      };
    }

    return {
      fields,
      checkboxesFields: [
        "preferential_right",
        "characteristic_handed_over",
        "criminal_record_handed_over",
        "passport_handed_over",
        "registration_certificate_handed_over",
        "university_card_handed_over",
        "application_handed_over",
      ],
    };
  },
  methods: {
    checkGrade(id, key, index, field) {
      let value = this.data[index][field];
      if (value > 10) value = 10;
      if (value < 0) value = 0;
      value = Math.round(value * 100) / 100;
      // todo
      /* eslint-disable vue/no-mutating-props */
      this.data[index][field] = value;
      /* eslint-enable vue/no-mutating-props */
      this.onUpdate(id, key, value);
    },
    onUpdate(id, key, value) {
      this.$emit("update", { id, key, value });
    },
  },
};
</script>

<style lang="scss" module>
.label {
  word-break: break-word !important;
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
