<template>
  <InputsBase
    :title="title"
    :wrapper-class-name="wrapperClassName"
    :title-class-name="titleClassName"
  >
    <el-switch
      v-model="value"
      v-bind="$attrs"
    />
  </InputsBase>
</template>

<script>
import { Component, Prop } from "vue-property-decorator";

import InputsMixin from "./inputsMixin";

@Component({
  name: "SwitchInput",
})
class SwitchInput extends InputsMixin {
  @Prop({ default: true }) trueValue
  @Prop({ default: false }) falseValue

  get value() {
    return this.modelValue === this.trueValue;
  }

  set value(newValue) {
    console.log("newValue", newValue);
    this.$emit("change", newValue ? this.trueValue : this.falseValue);
  }
}

export default SwitchInput;
</script>
