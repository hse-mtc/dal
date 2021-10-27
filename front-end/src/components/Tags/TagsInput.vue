<template>
  <ElFormItem :label="label">
    <ElTag
      v-for="selectedTag in selected"
      :key="selectedTag"
      closable
      class="mr-2"
      @close="handleClose(selectedTag)"
    >
      {{ selectedTag }}
    </ElTag>

    <ElAutocomplete
      v-model="tag"
      :fetch-suggestions="suggestions"
      class="inline-input"
      @select="handleSelect"
      @keyup.enter.native="handleSelect"
    />
  </ElFormItem>
</template>

<script>
import { getExistingTags } from "@/api/existingTags";

export default {
  name: "TagsInput",
  model: {
    prop: "selected",
    event: "change",
  },

  props: {
    label: {
      type: String,
      default: "Ключевые слова",
    },
    selected: {
      type: Array,
      default: () => [],
    },
  },

  data() {
    return {
      tag: "",
      all: [],
    };
  },

  created() {
    this.getSuggestions();
  },

  methods: {
    updateModel() {
      this.$emit("change", this.selected);
    },

    handleSelect() {
      const tag = this.tag.trim().toLowerCase();
      if (this.tag && !this.selected.includes(tag)) {
        // todo
        // eslint-disable-next-line vue/no-mutating-props
        this.selected.push(tag);
      }
      this.tag = "";

      this.updateModel();
    },

    handleClose(tag) {
      const index = this.selected.indexOf(tag);
      if (index > -1) {
        // todo
        // eslint-disable-next-line vue/no-mutating-props
        this.selected.splice(index, 1);
      }

      this.updateModel();
    },

    suggestions(text, cb) {
      // Two-step filter:
      //   1. Filter tags that are not selected yet.
      //   2. Leave the ones that contain tag as substring.
      const asValues = this.all
        .filter(
          tag => !this.selected.includes(tag) && tag.indexOf(text.toLowerCase()) > -1,
        )
        .map(tag => ({ value: tag }));

      cb(asValues);
    },

    async getSuggestions() {
      try {
        this.all = (await getExistingTags()).data;
      } catch (e) {
        this.$message.error("Не удалось загрузить тэги");
      }
    },
  },
};
</script>
