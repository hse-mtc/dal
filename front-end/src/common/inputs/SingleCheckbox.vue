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
import { Component, Prop } from "vue-property-decorator";

import InputsMixin from "./inputsMixin";

@Component({
  name: "SingleCheckbox",
})
class SingleCheckbox extends InputsMixin {
  @Prop({ type: String, default: "Да" }) checkboxLabel
}
export default SingleCheckbox;
</script>
