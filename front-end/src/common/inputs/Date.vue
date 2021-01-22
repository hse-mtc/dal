<template>
  <InputsBase
    :title="title"
    :wrapperClassName="wrapperClassName"
    :titleClassName="titleClassName"
  >
    <el-date-picker
      type="date"
      v-model="value"
      v-bind="$attrs"
      v-on="$listeners"
    />
  </InputsBase>
</template>

<script>
import mixin from './inputsMixin'

export default {
  mixins: [mixin],
  name: 'DateInput',
}
</script>
