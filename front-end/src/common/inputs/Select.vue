<template>
  <InputsBase
    v-if="options && options.length"
    :title="title"
    :wrapperClassName="wrapperClassName"
    :titleClassName="titleClassName"
  >
    <el-select
      v-model="value"
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
  name: 'Select',
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
