<template>
  <PrimeTable
    :value="data"
    class="p-datatable-gridlines p-datatable-striped p-datatable-sm"
    scrollable
    scroll-height="50vh"
    :edit-mode="newItemData ? 'row' : 'cell'"
    :row-class="row => row.newItem ? $style.addRow : ''"
    :frozen-value="newItemData"
    data-key="id"
    :editing-rows.sync="newItemData"
    @cell-edit-init="startEdit"
    @cell-edit-complete="stopEdit"
  >
    <template v-if="!newItemData" #header>
      <el-button
        icon="el-icon-plus"
        type="primary"
        style="width: 100%"
        @click="startAdd"
      >
        Добавить новый элемент
      </el-button>
    </template>

    <PrimeColumn
      v-for="({ title, width, editorType, props }, field) in columns"
      :key="field"
      :column-key="field"
      :header="title"
      :header-style="width ? `width: ${width}px;`: ''"
      :body-style="width ? `width: ${width}px;`: ''"
      :body-class="editorType ? $style.editableField : ''"
      :field="field"
    >
      <template #body="{ data }">
        <template v-if="editorType === 'checkbox'">
          {{ data[field] ? 'Да' : 'Нет' }}
        </template>
        <template v-else-if="editorType === 'select'">
          {{ getOptionLabel(data[field], props.options) }}
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
          @change="onEdit(field, $event, editorData.newItem)"
        />

        <TextInput
          v-else-if="editorType === 'input'"
          v-model="editorData[field]"
          @change="onEdit(field, $event, editorData.newItem)"
        />

        <SelectInput
          v-else-if="editorType === 'select'"
          v-model="editorData[field]"
          v-bind="props"
          @change="onEdit(field, $event, editorData.newItem)"
        />
      </template>
    </PrimeColumn>

    <PrimeColumn
      column-key="button"
      header="Удалить"
    >
      <template #body="{ data }">
        <el-button
          circle
          :disabled="!!newItemData"
          type="danger"
          icon="el-icon-close"
          @click="$emit('delete', data.id)"
        />
      </template>

      <template
        v-if="!!newItemData"
        #editor="{ data }"
      >
        <el-button
          circle
          icon="el-icon-check"
          type="primary"
          @click="addItem(data)"
        />
        <el-button
          circle
          icon="el-icon-close"
          type="danger"
          @click="stopAdd"
        />
      </template>
    </PrimeColumn>
  </PrimeTable>
</template>

<script>
import { Component, Prop } from "vue-property-decorator";

import { SingleCheckbox, TextInput, SelectInput } from "@/common/inputs";
import { ReferenceModule } from "@/store";

@Component({
  name: "DictionariesTableEditor",
  components: { SingleCheckbox, TextInput, SelectInput },
})
class DictionariesTableEditor {
  @Prop({ type: String, required: true }) type
  @Prop({ type: Array, required: true, default: () => [] }) data

  editingItemKey = undefined
  newItemData = null

  get columnsByTypes() {
    return {
      milgroups: {
        milgroup: { title: "Взвод", width: 100, editorType: "input" },
        milfaculty: {
          title: "Направление",
          width: 200,
          editorType: "select",
          props: { options: this.milfacultiesOptions },
        },
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
    };
  }

  get milfacultiesOptions() {
    return ReferenceModule.milfaculties.map(item => ({
      label: item.milfaculty,
      value: item.milfaculty,
    }));
  }

  get columns() { return this.columnsByTypes[this.type]; }

  getOptionLabel(item, options) {
    const currentOption = options.find(option => option.value === item);

    return currentOption ? currentOption.label : "";
  }

  startEdit({ data, field }) {
    this.editingItemKey = `${data.id} ${field}`;
    this.$emit("startEdit", data.id);
  }

  stopEdit({ data, field }) {
    if (this.editingItemKey === `${data.id} ${field}`) {
      this.$emit("abortEdit");
    }
  }

  onEdit(field, value, isNew) {
    if (!isNew) {
      this.$emit("submitEdit", { [field]: value });
    }
  }

  getNewItemInitData() {
    const fields = Object.keys(this.columns);

    const getInitValue = conf => {
      if (conf.editorType === "select") return conf.props.options[0].value;
      if (conf.editorType === "checkbox") return false;
      if (conf.editorType === "input") return "";
      return "";
    };

    return fields.reduce((memo, field) => ({
      ...memo,
      [field]: getInitValue(this.columns[field]),
    }), { newItem: true });
  }

  startAdd() {
    this.newItemData = [this.getNewItemInitData()];
  }

  stopAdd() {
    this.newItemData = null;
  }

  addItem(data) {
    this.$emit("addItem", data);
    this.stopAdd();
  }
}

export default DictionariesTableEditor;
</script>

<style lang="scss" module>
@import "@/styles/variables.scss";

@keyframes highlight {
  from {
    background: #fff;
  }
  50% {
    background: #a7a6a6;
  }
  to {
    background: #fff;
  }
}

.addRow {
  animation: highlight 1.5s linear 1;
}

.editableField {
  cursor: pointer;

  &:hover {
    color: $darkBlue;
  }
}
</style>
