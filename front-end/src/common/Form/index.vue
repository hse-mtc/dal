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
      v-for="({ component, title, props = {}, display = (value) => value }, key) in fields"
      :key="key"
      :prop="key"
    >
      <component
        :is="components[component]"
        v-if="components[component]"
        :model-value="formData[key]"
        :title="title"
        :left-label="leftLabel"
        :label-width="labelWidth"
        v-bind="props"
        @change="onChange(key, $event)"
      />
      <InputsBaseInput
        v-else
        :title="title"
        :left-label="leftLabel"
        :label-width="labelWidth"
        v-bind="props"
      >
        <component
          :is="component"
          v-bind="getNotInputProps(props)"
        >
          {{ display(formData[key]) }}
        </component>
      </InputsBaseInput>
    </el-form-item>

    <el-form-item :class="$style.buttons">
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
  Vue,
} from "vue-property-decorator";

import _omit from "lodash/omit";

import {
  DateInput,
  FileInput,
  NumberInput,
  SelectInput,
  TagsInput,
  TextInput,
  SingleCheckbox,
  SwitchInput,
  InputsBaseInput,
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
    InputsBaseInput,
  },
})
class GenericForm extends Vue {
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

  getNotInputProps(props) {
    return _omit(props, [
      "annotation",
      "wrapperClassName",
      "titleClassName",
      "annotationClassName",
    ]);
  }
}

export default GenericForm;
</script>

<style lang="scss" module>
:global(.el-select-dropdown__item) {
  height: auto !important;
  white-space: normal;
}

.buttons {
  margin-bottom: 0;
}
</style>
