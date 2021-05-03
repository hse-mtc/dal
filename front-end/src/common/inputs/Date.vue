<template>
  <InputsBase
    :title="title"
    :annotation="annotation"
    :wrapper-class-name="wrapperClassName"
    :title-class-name="titleClassName"
    :annotation-class-name="annotationClassName"
  >
    <el-date-picker
      v-model="value"
      style="width: 100%; max-width: 100%"
      :type="type"
      v-bind="$attrs"
      :format="format"
      :value-format="valueFormat"
    />
  </InputsBase>
</template>

<script>
import mixin from "./inputsMixin";

export default {
  name: "DateInput",
  mixins: [mixin],
  props: {
    type: { type: String, default: "date" },
    format: { type: String, default: "dd.MM.yyyy" },
    valueFormat: { type: String, default: "yyyy-MM-dd" },
  },
};
</script>
