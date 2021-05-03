<template>
  <InputsBase
    :title="title"
    :annotation="annotation"
    :wrapper-class-name="wrapperClassName"
    :title-class-name="titleClassName"
    :annotation-class-name="annotationClassName"
  >
    <el-select
      v-model="value"
      style="width: 100%; max-width: 100%"
      v-bind="$attrs"
    >
      <el-option
        v-for="{label, optionValue} in selectOptions"
        :key="optionValue"
        :value="optionValue"
        :label="label"
      />
    </el-select>
  </InputsBase>
</template>

<script>
import _isObject from "lodash/isObject";
import _isArray from "lodash/isArray";
import mixin from "./inputsMixin";

export default {
  name: "SelectInput",
  mixins: [mixin],
  props: {
    options: { type: Array, default: () => [] },
  },
  computed: {
    selectOptions() {
      return this.options.map(option => {
        const isObj = _isObject(option);
        const rawLabel = isObj ? option.label : option;

        return {
          label: _isObject(rawLabel) ? JSON.stringify(rawLabel) : rawLabel,
          value: JSON.stringify(isObj ? option.value : option),
        };
      });
    },

    value: {
      get() {
        if (_isArray(this.modelValue)) {
          return this.modelValue.map(item => this.encodeValue(item));
        }

        return this.encodeValue(this.modelValue);
      },
      set(newValue) {
        if (_isArray(newValue)) {
          this.$emit(
            "change",
            newValue.map(item => this.decodeValue(item)),
          );
        }

        this.$emit("change", this.decodeValue(newValue));
      },
    },
  },
  methods: {
    encodeValue(value) {
      if (!value && value !== 0) return value;
      return JSON.stringify(value);
    },
    decodeValue(value) {
      if (!value && value !== 0) return value;
      return JSON.parse(value);
    },
  },
};
</script>
