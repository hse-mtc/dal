<template>
  <el-form
    ref="form"
    :class="$style.root"
    :model="formData"
    :rules="rules"
    action="#"
    @submit.native.prevent="validate"
    @keypress.enter.native.prevent="validate"
  >
    <el-form-item
      v-for="({ component, title, props = {} }, key) in fields"
      :key="key"
      :prop="key"
    >
      <component
        :is="components[component]"
        :model-value="formData[key]"
        :title="title"
        :left-label="leftLabel"
        :label-width="labelWidth"
        v-bind="props"
        @change="onChange(key, $event)"
      />
    </el-form-item>

    <el-form-item>
      <slot name="buttons" :validate="validate" />
    </el-form-item>
  </el-form>
</template>

<script>
import {
  Component,
  Emit,
  Model,
  Prop,
  Ref,
} from "vue-property-decorator";

import {
  DateInput,
  FileInput,
  NumberInput,
  SelectInput,
  TagsInput,
  TextInput,
  SingleCheckbox,
  SwitchInput,
} from "@/common/inputs";

@Component({
  name: "GenericForm",
  components: {
    DateInput,
    FileInput,
    NumberInput,
    SelectInput,
    TagsInput,
    TextInput,
    SingleCheckbox,
    SwitchInput,
  },
})
class GenericForm {
  @Model("change", { type: Object, required: true }) formData
  @Prop({ type: Object, required: true, default: () => ({}) }) fields
  @Prop({ type: Object, default: () => ({}) }) rules
  @Prop({ type: Function, default: () => {} }) onSubmit
  @Prop({ type: Boolean }) leftLabel
  @Prop({ default: "auto" }) labelWidth

  @Ref() form

  components = {
    date: DateInput,
    file: FileInput,
    number: NumberInput,
    select: SelectInput,
    tags: TagsInput,
    text: TextInput,
    checkbox: SingleCheckbox,
    switch: SwitchInput,
  }

  @Emit("change")
  onChange(field, value) {
    return {
      ...this.formData,
      [field]: value,
    };
  }

  validate() {
    let isValid = false;

    this.form.validate(valid => {
      if (valid) {
        this.onSubmit();

        isValid = true;
      } else {
        this.$message({
          type: "error",
          message: "Проверьте правильность заполняемых полей",
        });

        isValid = false;
      }
    });

    return isValid;
  }
}

export default GenericForm;
</script>

<style lang="scss" module>
:global(.el-select-dropdown__item) {
  height: auto !important;
  white-space: normal;
}
</style>