<template>
  <div :class="$style.root">
    <el-table :data="data" border>
      <el-table-column
        v-for="({title, width}, field) in fields"
        :key="field"
        :prop="field"
        :label="title"
        :width="width"
        :fixed="field === 'fullName'"
      >
        <template slot-scope="{row, $index}">
          <template v-if="field === 'healthStatus'">
            <SelectInput
              v-model="data[$index][field]"
              :options="[
                { label: 'Годен', value: 1 },
                { label: 'Не годен', value: 2 },
              ]"
              :clearable="true"
            />
          </template>

          <template v-else-if="field === 'psychoStatus'">
            <SelectInput
              v-model="row[field]"
              :options="[
                { label: 'I', value: 1 },
                { label: 'II', value: 2 },
                { label: 'III', value: 3 },
                { label: 'IV', value: 4 },
                { label: 'V', value: 5  },
              ]"
              :clearable="true"
            />
          </template>

          <template v-else-if="checkboxesFields.includes(field)">
            <SingleCheckbox
              v-model="row[field]"
              checkboxLabel="Есть"
            />
          </template>

          <template v-else>
            {{ row[field] }}
          </template>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { SelectInput, SingleCheckbox } from '@/common/inputs'

export default {
  name: 'ApplicantDocuments',
  components: {
    SelectInput,
    SingleCheckbox,
  },
  data() {
    return {
      fields: {
        fullName: { title: 'Фамилия, имя, отчество', width: 400 },
        birthday: { title: 'Дата рождения', width: 100 },
        milcode: { title: 'Код специальности (направление подготовки)' },
        healthStatus: { title: 'Результаты медицинского освидетельствования', width: 130 },
        psychoStatus: { title: 'Результаты профессионального психологического отбора' },
        advantage: { title: 'Преимущественное право' },
        characteristics: { title: 'Характеристика' },
        criminalRecord: { title: 'Справка о несудимости' },
        passport: { title: 'Паспорт' },
        milCert: { title: 'Приписное свидетельство' },
        universityId: { title: 'Студенческий билет' },
        application: { title: 'Заявление' },
        faculty: { title: 'Факультет' },
      },

      checkboxesFields: ['advantage', 'characteristics', 'criminalRecord', 'passport', 'milCert', 'universityId', 'application'],

      data: [
        {
          fullName: 'sdcskdcjnskc',
          birthday: '2020-12-12',
          milcode: '121212',
          healthStatus: '',
          psychoStatus: '',
          advantage: '',
          characteristics: '',
          criminalRecord: '',
          passport: '',
          milCert: '',
          universityId: '',
          application: '',
          faculty: '',
        },
      ],
    };
  },
}
</script>

<style lang="scss" module>
.root {
  padding: 50px;
}

.label {
  height: 150px;
  word-break: break-word !important;

  &.verticalText {
    writing-mode: vertical-rl;
  }
}

</style>
