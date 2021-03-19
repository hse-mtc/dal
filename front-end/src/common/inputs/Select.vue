<template>
  <InputsBase
    :title="title"
    :annotation="annotation"
    :wrapperClassName="wrapperClassName"
    :titleClassName="titleClassName"
    :annotationClassName="annotationClassName"
  >
    <el-select
      style="width: 100%; max-width: 100%"
      v-model="value"
      v-bind="$attrs"
      v-on="$listeners"
    >
      <el-option
        v-for="option in selectOptions"
        :key="option.value"
        :label="option.label"
        :value="option.value"
      />
    </el-select>
  </InputsBase>
</template>

<script>
import mixin from "./inputsMixin";

export default {
  mixins: [mixin],
  name: "SelectInput",
  props: {
    options: { type: Array, default: () => [] },
  },
  computed: {
    // value: {
    //   get() {
    //     // console.log(this.modelValue
    //     //   ? JSON.stringify(this.modelValue)
    //     //   : this.modelValue)

    //     // return this.modelValue
    //     //   ? JSON.stringify(this.modelValue)
    //     //   : this.modelValue

    //     if (this.lodash.isArray(this.modelValue)) {
    //       return this.modelValue.map((item) => this.isObject(item) ? JSON.stringify(item) : item)
    //     }

    //     if (!this.modelValue && this.modelValue !== 0) return ''

    //     return this.isObject(this.modelValue) ? JSON.stringify(this.modelValue) : this.modelValue
    //   },
    //   set(value) {
    //     // const newVal = rawValue ? JSON.parse(rawValue) : rawValue 
    //     // console.log(newVal)
    //     // this.$emit('change', newVal)

    //     let newValue
    //     if (this.lodash.isArray(value)) {
    //       newValue = value.map((item) => this.isObject(item) ? item : JSON.parse(item))
    //     } else {
    //       newValue = JSON.parse(this.isObject(value) ? value : JSON.parse(value))
    //     }

    //     this.$emit('change', newValue)
    //   }
    // },
    selectOptions() {
      return this.options.map((option) => this.optionData(option))
    }
  },
  methods: {
    isObject(item) {
      return !this.lodash.isString(item) && !this.lodash.isNumber(item);
    },
    optionData(option) {
      const isObj = this.isObject(option);

      return {
        value: isObj && option.value ? JSON.stringify(option.value) : option,
        label: isObj ? option.label : option,
      };
    },
  },
};
</script>
