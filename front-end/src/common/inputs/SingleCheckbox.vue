<template>
  <InputsBase
    :title="title"
    :wrapper-class-name="wrapperClassName"
    :title-class-name="titleClassName"
  >
    <el-checkbox v-model="value" v-bind="$attrs" :label="checkboxLabel" />
  </InputsBase>
</template>

<script>
import mixin from "./inputsMixin";

export default {
  name: "SingleCheckbox",
  mixins: [mixin],
  props: {
    checkboxLabel: {
      type: String,
      default: "Да",
    },
  },
};
</script>
