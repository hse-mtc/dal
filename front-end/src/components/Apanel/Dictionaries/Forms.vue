<template>
  <ElForm
    ref="form"
    :key="reloadKey"
    :model="dataByTypes[type]"
    :rules="rulesByTypes[type]"
    action="#"
    @submit.native.prevent="onSubmit"
    @keypress.enter.native.prevent="onSubmit"
  >
    <ElFormItem
      v-for="({ placeholder }, field) in fieldsByTypes[type]"
      :key="field"
      :prop="field"
    >
      <el-input
        v-model="dataByTypes[type][field]"
        :placeholder="placeholder"
      />
    </ElFormItem>

    <el-button
      type="primary"
      @click="onSubmit"
    >
      {{ isEdit ? 'Изменить' : 'Добавить' }}
    </el-button>

    <el-button
      v-if="isEdit"
      @click="$emit('cancel')"
    >
      Отменить
    </el-button>
  </ElForm>
</template>

<script>
import { Component, Prop, Watch } from "vue-property-decorator";
import _cloneDeep from "lodash/cloneDeep";

@Component({
  name: "DictionariesForms",
})
class DictionariesForms {
  @Prop({ type: String }) type
  @Prop({ type: Object, default: () => ({}) }) initState
  @Prop({ type: Boolean }) isEdit

  reloadKey = 0

  dataByTypes = {
    publishers: {
      name: "",
    },
    authors: {
      surname: "",
      name: "",
      patronymic: "",
    },
    categories: {
      title: "",
    },
  }

  fieldsByTypes = {
    publishers: {
      name: { placeholder: "Введите нового издателя" },
    },
    authors: {
      surname: { placeholder: "Введите фамилию" },
      name: { placeholder: "Введите имя" },
      patronymic: { placeholder: "Введите отчество" },
    },
    categories: {
      title: { placeholder: "Введите название" },
    },
  }

  rulesByTypes = {
    publishers: {
      name: [{ required: true, message: "Обязательное поле" }],
    },
    authors: {
      surname: [{ required: true, message: "Обязательное поле" }],
      name: [{ required: true, message: "Обязательное поле" }],
      patronymic: [],
    },
    categories: {
      title: [{ required: true, message: "Обязательное поле" }],
    },
  }

  onSubmit(e) {
    if (e) e.preventDefault();

    const data = this.dataByTypes[this.type];
    const keys = Object.keys(data);
    keys.forEach(key => {
      data[key] = data[key].trim().toLowerCase();
    });

    this.$refs.form.validate(valid => {
      if (valid) {
        this.$emit(
          this.isEdit ? "change" : "submit",
          data,
        );
        this.dataByTypes[this.type] = {};
        this.reloadKey += 1;
      }
    });
  }

  initEdit() {
    this.dataByTypes[this.type] = this.isEdit
      ? _cloneDeep(this.initState)
      : {};

    this.reloadKey += 1;
  }

  @Watch("initState", { deep: true })
  onInitStateChange() { this.initEdit(); }

  @Watch("isEdit", { deep: true })
  onIsEditChange() { this.initEdit(); }
}

export default DictionariesForms;
</script>

<style lang="scss" module>
.root {}
</style>
