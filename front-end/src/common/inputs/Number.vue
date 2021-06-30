<template>
  <InputsBase
    :title="title"
    :wrapper-class-name="wrapperClassName"
    :title-class-name="titleClassName"
  >
    <el-input-number
      v-model="value"
      style="width: 100%; max-width: 100%"
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
