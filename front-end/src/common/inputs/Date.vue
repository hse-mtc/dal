<template>
  <InputsBase
    :title="title"
    :wrapperClassName="wrapperClassName"
    :titleClassName="titleClassName"
  >
    <el-date-picker
      type="date"
      v-model="value"
    />
  </InputsBase>
</template>

<script>
import mixin from './inputsMixin'

export default {
  mixins: [mixin],
  name: 'Date',
}
</script>
