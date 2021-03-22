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
import _isArray from "lodash/isArray";

export default {
  mixins: [mixin],
  name: "SelectInput",
  props: {
    options: { type: Array, default: () => [] },
  },
  computed: {
    value: {
      get() {
        if (_isArray(this.modelValue)) {
          return this.modelValue.map((item) => JSON.stringify(item));
        }

        if (!this.modelValue && this.modelValue !== 0) return "";

        return JSON.stringify(this.modelValue);
      },
      set(value) {
        let newValue;
        if (_isArray(value)) {
          newValue = value.map((item) => JSON.parse(item));
        } else {
          newValue = JSON.parse(value);
        }

        console.log(`newValue`, newValue);
        this.$emit("change", newValue);
      },
    },
    selectOptions() {
      return this.options.map((option) => this.optionProps(option));
    },
  },
  methods: {
    isObject(item) {
      return !this.lodash.isString(item) && !this.lodash.isNumber(item);
    },
    optionProps(item) {
      const value = JSON.stringify(this.isObject(item) ? item.value : item);
      const label = `${this.isObject(item) ? item.label : item}`;

      return { value, label };
    },
  },
};
</script>
