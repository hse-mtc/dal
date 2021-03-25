<template>
  <InputsBase
    :title="title"
    :annotation="annotation"
    :wrapperClassName="wrapperClassName"
    :titleClassName="titleClassName"
    :annotationClassName="annotationClassName"
  >
    <el-date-picker
      style="width: 100%; max-width: 100%"
      :type="type"
      v-model="value"
      v-bind="$attrs"
      format="dd.MM.yyyy"
      value-format="yyyy-MM-dd"
    />
  </InputsBase>
</template>

<script>
import mixin from "./inputsMixin";

export default {
  mixins: [mixin],
  name: "DateInput",
  props: {
    type: { type: String, default: "date" },
  },
};
</script>
