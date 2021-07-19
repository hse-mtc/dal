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
    <el-input
      v-model="value"
      style="width: 100%; max-width: 100%"
      :type="type"
      v-bind="$attrs"
      :placeholder="placeholder"
      v-on="listeners"
    />
  </InputsBase>
</template>

<script>
import { Component, Prop } from "vue-property-decorator";
import _omit from "lodash/omit";

import InputsMixin from "./inputsMixin";

@Component({
  name: "TextInput",
})
class TextInput extends InputsMixin {
  @Prop({ type: Boolean }) isTextArea
  @Prop({ type: Boolean }) onlyChars
  @Prop({ type: String, default: "" }) placeholder

  get value() { return this.modelValue; }

  get type() {
    return this.isTextArea ? "textarea" : "text";
  }

  set value(value) {
    this.$emit("change", this.onlyChars ? value.replace(/\d/g, "") : value);
  }

  get listeners() {
    return _omit(this.$listeners, ["change"]);
  }
}

export default TextInput;
</script>
