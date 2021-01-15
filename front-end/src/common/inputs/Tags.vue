<template>
  <InputsBase
    :title="title"
    :wrapperClassName="wrapperClassName"
    :titleClassName="titleClassName"
  >
    <el-tag
      v-for="tag in value"
      :key="tag"
      closable
      @close="handleClose(tag)"
    >
      {{ tag }}
    </el-tag>

    <el-autocomplete
      v-model="tag"
      :fetch-suggestions="filterSuggestions"
      @select="handleSelect"
      @keyup.enter.native="handleSelect"
      class="inline-input"
    />
  </InputsBase>
</template>

<script>
import mixin from './inputsMixin'

export default {
  mixins: [mixin],
  name: "TagsInput",
  props: {
    suggestions: {type: Array, default: () => []},
  },
  data() {return  {tag: ''}},
  methods: {
    handleSelect() {
      const newTag = this.tag.trim().toLowerCase();
      if (newTag && !this.value.includes(newTag)) {
        this.value = [...this.value, newTag];
      }
      this.tag = "";
    },

    handleClose(tag) {
      this.value = this.lodash.filter(
        this.value,
        (item) => item !== tag
      )
    },

    filterSuggestions(text, cb) {
      // Two-step filter:
      //   1. Filter tags that are not selected yet.
      //   2. Leave the ones that contain tag as substring.
      cb(this.lodash.filter(
        this.suggestions,
        (tag) => !this.value.includes(tag) && tag.indexOf(text.trim().toLowerCase()) > -1
      ).map((tag) => ({ value: tag })));
    },
  },
};
</script>
