<template>
  <InputsBase
    :title="title"
    :wrapperClassName="wrapperClassName"
    :titleClassName="titleClassName"
  >
    <el-checkbox v-model="value" v-bind="$attrs" :label="checkboxLabel" />
  </InputsBase>
</template>

<script>
import mixin from "./inputsMixin";

export default {
  mixins: [mixin],
  name: "SingleCheckbox",
  props: {
    checkboxLabel: {
      type: String,
      default: "Да",
    },
  },
};
</script>
