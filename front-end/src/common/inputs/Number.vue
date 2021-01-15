<template>
  <InputsBase
    :title="title"
    :wrapperClassName="wrapperClassName"
    :titleClassName="titleClassName"
  >
    <el-input
      v-model="value"
      type="number"
    />
  </InputsBase>
</template>

<script>
import mixin from './inputsMixin'

export default {
  mixins: [mixin],
  name: 'Text',
}
</script>
