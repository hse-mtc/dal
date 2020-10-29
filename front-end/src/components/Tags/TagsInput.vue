<template>
  <el-form-item :label="label">
    <el-tag
        v-for="tag in selected"
        :key="tag"
        closable
        @close="handleClose(tag)"
        class="mr-2"
    >
      {{ tag }}
    </el-tag>

    <el-autocomplete
        v-model="tag"
        :fetch-suggestions="suggestions"
        @select="handleSelect"
        @keyup.enter.native="handleSelect"
        class="inline-input"
    ></el-autocomplete>
  </el-form-item>
</template>

<script>
import {getExistingTags} from "@/api/existingTags";

export default {
  name: "TagsInput",

  props: {
    label: {
      type: String,
      required: true,
    },
    selected: {
      type: Array,
      default: () => []
    }
  },

  data() {
    return {
      tag: '',
      all: [],
    }
  },

  created() {
    getExistingTags()
      .then(response => {
        this.all = response.data
      })
      .catch(error => {
        console.log("Failed to fetch tags: ", error)
      })
  },

  methods: {
    handleSelect() {
      const tag = this.tag.trim().toLowerCase()
      if (this.tag && !this.selected.includes(tag)) {
        this.selected.push(tag)
      }
      this.tag = ''
    },

    handleClose(tag) {
      const index = this.selected.indexOf(tag)
      if (index > -1) {
        this.selected.splice(index, 1)
      }
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
