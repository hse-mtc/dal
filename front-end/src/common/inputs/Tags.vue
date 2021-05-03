<template>
  <Select
    v-model="value"
    :title="title"
    :annotation="annotation"
    :wrapper-class-name="wrapperClassName"
    :title-class-name="titleClassName"
    :annotation-class-name="annotationClassName"
    :options="tags"
    multiple
    filterable
    allow-create
    default-first-option
    @change="onChange"
  />
</template>

<script>
import mixin from "./inputsMixin";
import Select from "./Select.vue";

export default {
  name: "TagsInput",
  components: { Select },
  mixins: [mixin],
  props: {
    tags: { type: Array, default: () => [] },
  },
  data() {
    return { tag: "" };
  },
  methods: {
    onChange(values) {
      this.$emit(
        "change",
        values
          .map(item => item.trim().toLowerCase())
          .filter(item => Boolean(item)),
      );
    },
  },
};
</script>
