<template>
  <InputsBase
    :title="title"
    :annotation="inputAnnotation"
    :wrapper-class-name="wrapperClassName"
    :title-class-name="titleClassName"
    :annotation-class-name="annotationClassName"
    :left-label="leftLabel"
    :label-width="labelWidth"
  >
    <el-upload
      action=""
      :auto-upload="false"
      :limit="limit"
      :file-list="value"
      :on-change="onChange"
      :on-remove="onChange"
      :accept="filesTypes.join()"
      v-bind="$attrs"
    >
      <el-button
        :disabled="value && value.length === limit"
        size="small"
        type="primary"
      >
        Выберите файл
      </el-button>
    </el-upload>
  </InputsBase>
</template>

<script>
import { Component, Prop } from "vue-property-decorator";

import InputsMixin from "./inputsMixin";

@Component({
  name: "FileInput",
})
class FileInput extends InputsMixin {
  @Prop({ type: Number, default: 0 }) limit
  @Prop({ type: Array, default: () => [] }) filesTypes

  get inputAnnotation() {
    if (this.lodash.isString(this.annotation) || !this.filesTypes.length) {
      return this.annotation;
    }

    return `Файлы в формате ${this.filesTypes.slice(0, -1).join(", ")}${
      this.filesTypes.length !== 1 ? " или " : ""
    }${this.filesTypes.slice(-1)}`;
  }

  onChange(file, files) {
    this.value = files;
  }
}

export default FileInput;
</script>
