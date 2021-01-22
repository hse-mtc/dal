<template>
  <InputsBase
    :title="title"
    :annotation="inputAnnotation"
    :wrapperClassName="wrapperClassName"
    :titleClassName="titleClassName"
    :annotationClassName="annotationClassName"
  >
    <el-input
      v-model="value"
      :type="type"
      v-bind="$attrs"
      v-on="$listeners"
    />
  </InputsBase>
</template>

<script>
import mixin from './inputsMixin'

export default {
  mixins: [mixin],
  name: 'TextInput',
  props: {
    isTextArea: {type: Boolean, default: false},
  },
  computed: {
    type() {
      return this.isTextArea
        ? 'textarea'
        : 'text'
    }
  }
}
</script>
