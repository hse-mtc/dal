<template>
  <ElFormItem :label="label">
    <ElTag
        v-for="tag in selected"
        :key="tag"
        closable
        @close="handleClose(tag)"
        class="mr-2"
    >
      {{ tag }}
    </ElTag>

    <ElAutocomplete
        v-model="tag"
        :fetch-suggestions="suggestions"
        @select="handleSelect"
        @keyup.enter.native="handleSelect"
        class="inline-input"
    />
  </ElFormItem>
</template>

<script>
import {getExistingTags} from "@/api/existingTags";

export default {
  name: "TagsInput",
  model: {
    prop: "selected",
    event: "change",
  },

  props: {
    label: {
      type: String,
      default: "Ключевые слова"
    },
    selected: {
      type: Array,
      default: () => [],
    },
  },

  data() {
    return {
      tag: '',
      all: [],
    }
  },

  async created() {
    try {
      this.all = (await getExistingTags()).data
    } catch (error) {
      console.log("Failed to fetch Tags: ", error)
    }
  },

  methods: {
    updateModel() {
      this.$emit("change", this.selected)
    },

    handleSelect() {
      const tag = this.tag.trim().toLowerCase()
      if (this.tag && !this.selected.includes(tag)) {
        this.selected.push(tag)
      }
      this.tag = ''

      this.updateModel()
    },

    handleClose(tag) {
      const index = this.selected.indexOf(tag)
      if (index > -1) {
        this.selected.splice(index, 1)
      }

      this.updateModel()
    },

    suggestions(text, cb) {
      // Two-step filter:
      //   1. Filter tags that are not selected yet.
      //   2. Leave the ones that contain tag as substring.
      const asValues = this.all
      .filter(tag => !this.selected.includes(tag) && tag.indexOf(text.toLowerCase()) > -1)
      .map(tag => ({value: tag}))

      cb(asValues)
    },
  }
}
</script>
