<template>
  <InputsBase
    :title="title"
    :annotation="annotation"
    :wrapperClassName="wrapperClassName"
    :titleClassName="titleClassName"
    :annotationClassName="annotationClassName"
  >
    <el-input
      style="width: 100%; max-width: 100%"
      v-model="value"
      :type="type"
      v-bind="$attrs"
      v-on="$listeners"
    />
  </InputsBase>
</template>

<script>
import mixin from "./inputsMixin";

export default {
  mixins: [mixin],
  name: "TextInput",
  props: {
    isTextArea: { type: Boolean, default: false },
    onlyChars: { type: Boolean, default: false },
  },
  computed: {
    type() {
      return this.isTextArea ? "textarea" : "text";
    },
    value: {
      get() { return this.modelValue },
      set(value) {
        this.$emit("change", this.onlyChars
          ? value.replace(/\d/g, '')
          : value
        );
      },
    }
  },
};
</script>
