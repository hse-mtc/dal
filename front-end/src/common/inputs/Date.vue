<template>
  <InputsBase
    :title="title"
    :annotation="inputAnnotation"
    :wrapperClassName="wrapperClassName"
    :titleClassName="titleClassName"
    :annotationClassName="annotationClassName"
  >
    <el-date-picker
      style="max-width: 100%;"
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
