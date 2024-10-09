<template>
  <InputsBase
    :title="title"
    :annotation="annotation"
    :wrapper-class-name="wrapperClassName"
    :title-class-name="titleClassName"
    :annotation-class-name="annotationClassName"
    :left-label="leftLabel"
    :label-width="labelWidth"
  >
    <el-select
      v-model="value"
      style="width: 100%; max-width: 100%"
      v-bind="$attrs"
    >
      <el-option
        v-for="{ label, optionValue, class_ } in selectOptions"
        :key="optionValue"
        :value="optionValue"
        :label="label"
        :class="class_"
      />
    </el-select>
  </InputsBase>
</template>

<script>
import { Component, Prop } from "vue-property-decorator";

import _isObject from "lodash/isObject";
import _isArray from "lodash/isArray";

import InputsMixin from "./inputsMixin";

@Component({
  name: "SelectInput",
})
class SelectInput extends InputsMixin {
  @Prop({ type: Array, default: () => [] }) options

  get selectOptions() {
    return this.options.map(option => {
      const isObj = _isObject(option);
      const rawLabel = isObj ? option.label : option;

      const getValue = item => {
        if (isObj) {
          if (_isObject(item.value)) { return JSON.stringify(item.value); }

          return item.value;
        }

        return item;
      };

      return {
        label: _isObject(rawLabel) ? JSON.stringify(rawLabel) : rawLabel,
        optionValue: getValue(option),
        class_: option.class
      };
    });
  }

  get value() {
    if (_isArray(this.modelValue)) {
      return this.modelValue.map(item => this.encodeValue(item));
    }

    return this.encodeValue(this.modelValue);
  }

  set value(newValue) {
    if (_isArray(newValue)) {
      this.$emit(
        "change",
        newValue
          .map(item => this.decodeValue(item))
          .filter((item, index, arr) => arr.indexOf(item) === index),
      );
    } else {
      this.$emit("change", this.decodeValue(newValue));
    }
  }

  encodeValue(value) {
    if (!value && value !== 0) { return value; }

    if (_isObject(value)) {
      return JSON.stringify(value);
    }

    return value;
  }

  decodeValue(value) {
    if (!value && value !== 0) { return value; }
    try {
      return JSON.parse(value);
    } catch (e) {
      return value;
    }
  }
}

export default SelectInput;
</script>
