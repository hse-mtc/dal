<template>
  <InputsBase
    :title="title"
    :annotation="annotation"
    :wrapper-class-name="wrapperClassName"
    :title-class-name="titleClassName"
    :annotation-class-name="annotationClassName"
    :left-label="leftLabel"
    :label-width="labelWidth"
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
import { Component, Prop } from "vue-property-decorator";

import InputsMixin from "./inputsMixin";

@Component({
  name: "DateInput",
})
class DateInput extends InputsMixin {
  @Prop({ type: String, default: "date" }) type
  @Prop({ type: String, default: "dd.MM.yyyy" }) format
  @Prop({ type: String, default: "yyyy-MM-dd" }) valueFormat
}

export default DateInput;
</script>
