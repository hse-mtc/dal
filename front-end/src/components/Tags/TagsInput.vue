<template>
  <ElFormItem v-loading="fetchingTags" :label="label">
    <ElTag
      v-for="selectedTag in selectedTags"
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

<script lang="ts">
import {
  Component, Model, Prop, Vue,
} from "vue-property-decorator";

import { getExistingTags } from "@/api/existingTags";

type Suggestion = {
  value: string;
};

@Component({
  name: "TagsInput",
})
class TagsInput extends Vue {
  @Prop() label = "Ключевые слова";

  @Model("change", {
    type: Array,
    default: () => [],
  })
  readonly selectedTags!: string[];

  tag = "";
  allTags: string[] = [];
  fetchingTags = false;

  async created(): Promise<void> {
    await this.getTags();
  }

  async getTags(): Promise<void> {
    this.fetchingTags = true;
    try {
      this.allTags = (await getExistingTags()).data;
    } catch (error) {
      // FIXME(TmLev): Report error to user.
      console.log("Failed to fetch Tags: ", error);
    } finally {
      this.fetchingTags = false;
    }
  }

  suggestions(text: string, cb: (arg: Suggestion[]) => void): void {
    // Two-step filter:
    //   1. Filter tags that are not selected yet.
    //   2. Leave the ones that contain tag as substring.
    const asValues = this.allTags
      .filter(tag => !this.selectedTags.includes(tag) && tag.indexOf(text.toLowerCase()) > -1)
      .map(tag => ({ value: tag }));

    cb(asValues);
  }

  updateModel(): void {
    this.$emit("change", this.selectedTags);
  }

  handleSelect(): void {
    const tag = this.tag.trim().toLowerCase();
    if (tag && !this.selectedTags.includes(tag)) {
      this.selectedTags.push(tag);
    }
    this.tag = "";

    this.updateModel();
  }

  handleClose(tag: string): void {
    const index = this.selectedTags.indexOf(tag);
    if (index > -1) {
      this.selectedTags.splice(index, 1);
    }

    this.updateModel();
  }
}

export default TagsInput;
</script>
