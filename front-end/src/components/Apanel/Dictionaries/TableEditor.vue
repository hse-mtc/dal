<template>
  <PrimeTable
    :value="data"
    class="p-datatable-gridlines p-datatable-striped p-datatable-sm"
    scrollable
    scroll-height="50vh"
    edit-mode="cell"
  >
    <PrimeColumn
      v-for="({ title, width, editorType, props }, field) in columns"
      :key="field"
      :column-key="field"
      :header="title"
      :header-style="width ? `width: ${width}px;`: ''"
      :body-style="width ? `width: ${width}px;`: ''"
      :field="field === 'archived' ? (row => row.archived ? 'Да' : 'Нет') : field"
    >
      <template #body="{ data }">
        <template v-if="editorType === 'checkbox'">
          {{ data[field] ? 'Да' : 'Нет' }}
        </template>
        <template v-else-if="editorType === 'select'">
          {{ props && props.options.find(item => item.value === +data[field]).label }}
        </template>
        <template v-else>
          {{ data[field] }}
        </template>
      </template>

      <template
        v-if="editorType"
        #editor="{ data: editorData }"
      >
        <SingleCheckbox
          v-if="editorType === 'checkbox'"
          v-model="editorData[field]"
          :checkbox-label="editorData[field] ? 'Да' : 'Нет'"
        />

        <TextInput
          v-else-if="editorType === 'input'"
          v-model="editorData[field]"
        />

        <SelectInput
          v-else-if="editorType === 'select'"
          v-model="editorData[field]"
          v-bind="props"
        />
      </template>
    </PrimeColumn>

    <PrimeColumn
      column-key="button"
      header="Удалить"
    >
      <template #body>
        <el-button
          circle
          type="danger"
          icon="el-icon-close"
        />
      </template>
    </PrimeColumn>
  </PrimeTable>
</template>

<script>
import { Component, Prop } from "vue-property-decorator";

import { SingleCheckbox, TextInput, SelectInput } from "@/common/inputs";

@Component({
  name: "DictionariesTableEditor",
  components: { SingleCheckbox, TextInput, SelectInput },
})
class DictionariesTableEditor {
  @Prop({ type: String, required: true }) type
  @Prop({ type: Array, required: true, default: () => [] }) data

  columnsByTypes = {
    milgroups: {
      milgroup: { title: "Взвод", width: 100, editorType: "input" },
      milfaculty: { title: "Направление", width: 200/* , editorType: "select" */ },
      weekday: {
        title: "День посещения",
        width: 150,
        editorType: "select",
        props: {
          options: [
            { value: 0, label: "Понедельник" },
            { value: 1, label: "Вторник" },
            { value: 2, label: "Среда" },
            { value: 3, label: "Четверг" },
            { value: 4, label: "Пятница" },
            { value: 5, label: "Суббота" },
            { value: 6, label: "Воскресенье" },
          ],
        },
      },
      archived: { title: "Заархивирован", width: 150, editorType: "checkbox" },
    },
  }

  get columns() { return this.columnsByTypes[this.type]; }
}

export default DictionariesTableEditor;
</script>

<style lang="scss" module>
.root {}
</style>
