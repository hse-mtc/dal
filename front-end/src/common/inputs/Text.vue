<template>
  <InputsBase
    :title="title"
    :wrapperClassName="wrapperClassName"
    :titleClassName="titleClassName"
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
