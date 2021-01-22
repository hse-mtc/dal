<template>
  <InputsBase
    :title="title"
    :wrapperClassName="wrapperClassName"
    :titleClassName="titleClassName"
  >
    <el-upload
      action=""
      :auto-upload="false"
      :limit="limit"
      :file-list="value"
      :on-change="onChange"
      :on-remove="onChange"
      v-bind="$attrs"
      v-on="$listeners"
    >
      <el-button
        :disabled="value && value.length === limit" 
        size="small"
        type="primary"
      >
        Загрузить...
      </el-button>
    </el-upload>
  </InputsBase>
</template>

<script>
import mixin from './inputsMixin'

export default {
  mixins: [mixin],
  name: 'NumberInput',
  props: {limit: {type: Number}},
  methods: {
    onChange(file, files) {
      this.value = files
    }
  }
}
</script>
