<template>
  <InputsBase
    :title="title"
    :annotation="inputAnnotation"
    :wrapperClassName="wrapperClassName"
    :titleClassName="titleClassName"
    :annotationClassName="annotationClassName"
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
      v-on="$listeners"
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
import mixin from './inputsMixin'

export default {
  mixins: [mixin],
  name: 'NumberInput',
  props: {
    limit: {type: Number},
    filesTypes: {type: Array, default: () => []}
  },
  computed: {
    inputAnnotation() {
      if (this.lodash.isString(this.annotation) || !this.filesTypes.length) {
        return this.annotation
      }

      return `Файлы в формате ${this.filesTypes.slice(0, -1).join(', ')}${
        this.filesTypes.length !== 1
          ? ' или '
          : ''
      }${this.filesTypes.slice(-1)}`
    }
  },
  methods: {
    onChange(file, files) {
      this.value = files
    }
  }
}
</script>
