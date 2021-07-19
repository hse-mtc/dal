<template>
  <InputsBase
    :title="title"
    :wrapper-class-name="wrapperClassName"
    :title-class-name="titleClassName"
    :left-label="leftLabel"
    :label-width="labelWidth"
  >
    <PrimeNumberInput
      v-model="value"
      mode="decimal"
      :input-class="$style.input"
      v-bind="$attrs"
    />
  </InputsBase>
</template>

<script>
import { Component } from "vue-property-decorator";

import InputsMixin from "./inputsMixin";

@Component({
  name: "NumberInput",
})
class NumberInput extends InputsMixin {}

export default NumberInput;
</script>

<style lang="scss" module>
.input {
  width: 100%;
}
</style>
