<template>
  <InputsBase
    :title="title"
    :wrapperClassName="wrapperClassName"
    :titleClassName="titleClassName"
  >
    <el-input
      style="width: 100%; max-width: 100%"
      v-model="value"
      type="number"
      v-bind="$attrs"
      v-on="$listeners"
    />
  </InputsBase>
</template>

<script>
import mixin from './inputsMixin'

export default {
  mixins: [mixin],
  name: 'NumberInput',
}
</script>
