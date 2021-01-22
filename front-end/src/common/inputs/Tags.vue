<template>
  <Select
    :title="title"
    :annotation="annotation"
    :wrapperClassName="wrapperClassName"
    :titleClassName="titleClassName"
    :annotationClassName="annotationClassName"
    :options="tags"
    v-model="value"
    multiple
    filterable
    allow-create
    default-first-option
    @change="onChange"
  />
</template>

<script>
import mixin from './inputsMixin'
import Select from './Select.vue'

export default {
  mixins: [mixin],
  name: "TagsInput",
  components: {Select},
  props: {
    tags: {type: Array, default: () => []},
  },
  data() {return  {tag: ''}},
  methods: {
    onChange(values) {
      this.$emit('change', values
        .map(item => item.trim().toLowerCase())
        .filter(item => Boolean(item))
      )
    }
  },
};
</script>
