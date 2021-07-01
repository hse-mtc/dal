<template>
  <InputsBase
    :title="title"
    :wrapper-class-name="wrapperClassName"
    :title-class-name="titleClassName"
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
import mixin from "./inputsMixin";

export default {
  name: "NumberInput",
  mixins: [mixin],
};
</script>

<style lang="scss" module>
.input {
  width: 100%;
}
</style>
