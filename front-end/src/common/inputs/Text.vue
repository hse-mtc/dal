<template>
  <InputsBase
    :title="title"
    :annotation="annotation"
    :wrapper-class-name="wrapperClassName"
    :title-class-name="titleClassName"
    :annotation-class-name="annotationClassName"
  >
    <el-input
      v-model="value"
      style="width: 100%; max-width: 100%"
      :type="type"
      v-bind="$attrs"
      :placeholder="placeholder"
      v-on="$listeners"
    />
  </InputsBase>
</template>

<script>
import mixin from "./inputsMixin";

export default {
  name: "TextInput",
  mixins: [mixin],
  props: {
    isTextArea: { type: Boolean, default: false },
    onlyChars: { type: Boolean, default: false },
    placeholder: { type: String, default: "" },
  },
  computed: {
    type() {
      return this.isTextArea ? "textarea" : "text";
    },
    value: {
      get() {
        return this.modelValue;
      },
      set(value) {
        this.$emit("change", this.onlyChars ? value.replace(/\d/g, "") : value);
      },
    },
  },
};
</script>
