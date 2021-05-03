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

        <template v-else-if="fieZld === 'prof_psy_selection'">
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
    return {
      fields: {
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
        },
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
        },
        characteristic_handed_over: {
          abbr: "Хар-ка",
          title: "Характеристика",
        },
        criminal_record_handed_over: {
          abbr: "СН",
          title: "Справка о несудимости",
        },
        passport_handed_over: { title: "Паспорт", width: 100 },
        registration_certificate_handed_over: {
          abbr: "ПС",
          title: "Приписное свидетельство",
        },
        university_card_handed_over: {
          abbr: "СБ",
          title: "Студенческий билет",
        },
        application_handed_over: {
          title: "Заявление",
          width: 100,
        },
        faculty: {
          title: "Факультет",
          width: 100,
        },
      },

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
</style>
