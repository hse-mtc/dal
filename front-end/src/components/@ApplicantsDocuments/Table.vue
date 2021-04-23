<template>
  <el-table :data="data" border>
    <el-table-column
      v-for="({title, width}, field) in fields"
      :key="field"
      :prop="field"
      :label="title"
      :width="width"
      :fixed="field === 'fullName'"
      :label-class-name="$style.label"
    >
      <template slot-scope="{ row, $index }">
        <template v-if="field === 'medical_examination'">
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
        </template>

        <template v-else-if="field === 'prof_psy_selection'">
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
        </template>

        <template v-else-if="checkboxesFields.includes(field)">
          <SingleCheckbox
            v-model="data[$index][field]"
            checkboxLabel="Есть"
            @change="onUpdate(row.id, field, $event)"
          />
        </template>

        <template v-else>
          {{ row[field] }}
        </template>
      </template>
    </el-table-column>
  </el-table>
</template>

<script>
import { SelectInput, SingleCheckbox } from '@/common/inputs'

export default {
  name: 'ApplicantsDocuments',
  components: {
    SelectInput,
    SingleCheckbox,
  },
  props: {
    data: {
      required: true,
      type: Array,
      default: () => [],
    }
  },
  data() {
    return {
      fields: {
        fullname: { title: 'Фамилия, имя, отчество', width: 300 },
        birthday: { title: 'Дата рождения', width: 100 },
        program: { title: 'Код специальности (направление подготовки)' },
        medical_examination: { title: 'Результаты медицинского освидетельствования', width: 370 },
        prof_psy_selection: { title: 'Результаты профессионального психологического отбора' },
        preferential_right: { title: 'Преимущественное право' },
        characteristic_handed_over: { title: 'Характеристика' },
        criminal_record_handed_over: { title: 'Справка о несудимости' },
        passport_handed_over: { title: 'Паспорт' },
        registration_certificate_handed_over: { title: 'Приписное свидетельство' },
        university_card_handed_over: { title: 'Студенческий билет' },
        application_handed_over: { title: 'Заявление' },
        faculty: { title: 'Факультет' },
      },

      checkboxesFields: [
        'preferential_right',
        'characteristic_handed_over',
        'criminal_record_handed_over',
        'passport_handed_over',
        'registration_certificate_handed_over',
        'university_card_handed_over',
        'application_handed_over'
      ],
    };
  },
  methods: {
    onUpdate(id, key, value) {
      this.$emit('update', {id, key, value})
    }
  }
}
</script>

<style lang="scss" module>
.label {
  word-break: break-word !important;
}

</style>
