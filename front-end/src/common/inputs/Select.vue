<template>
  <InputsBase
    :title="title"
    :annotation="inputAnnotation"
    :wrapperClassName="wrapperClassName"
    :titleClassName="titleClassName"
    :annotationClassName="annotationClassName"
  >
    <el-select
      v-model="value"
      v-bind="$attrs"
      v-on="$listeners"
    >
      <!-- key в optionData(option) -->
      <!-- eslint-disable-next-line vue/valid-v-for -->
      <el-option
        v-for="option in options"
        v-bind="optionData(option)"
      />
    </el-select>
  </InputsBase>
</template>

<script>
import mixin from './inputsMixin'

export default {
  mixins: [mixin],
  name: 'SelectInput',
  props: {
    options: {type: Array, default: () => []},
  },
  methods: {
    isObject(item) {
      return !this.lodash.isString(item) && !this.lodash.isNumber(item)
    },
    optionData(option) {
      const isObj = this.isObject(option)

      return {
        key: isObj
          ? option.value
          : option,
        value: isObj
          ? option.value
          : option,
        label: isObj
          ? option.label
          : option,
      }
    }
  }
}
</script>
