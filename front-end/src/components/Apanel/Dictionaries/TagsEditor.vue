<template>
  <div :class="$style.tagsEditor">
    <div
      v-if="!editingItem"
      :class="$style.tagsWrapper"
    >
      <Tag
        v-for="({ id, title }) in tags"
        :id="id"
        :key="id"
        :title="title"
        :class="$style.tag"
        @delete="$emit('delete', id)"
        @edit="$emit('startEdit', id)"
      >
        {{ title }}
      </Tag>
    </div>

    <Forms
      :is-edit="!!editingItem"
      :init-state="editingItem"
      :type="type"
      :class="$style.tagsForm"
      @submit="$emit('addItem', $event)"
      @change="$emit('submitEdit', $event)"
      @cancel="$emit('abortEdit')"
    />
  </div>
</template>

<script>
import { Component, Prop, Vue } from "vue-property-decorator";

import Tag from "./Tag.vue";
import Forms from "./Forms.vue";

@Component({
  name: "DictionariesTagsEditor",
  components: { Tag, Forms },
})
class DictionariesTagsEditor extends Vue {
  @Prop({ type: String, required: true }) type
  @Prop({ type: Array, required: true, default: () => ({}) }) tags
  @Prop() editingItem
}

export default DictionariesTagsEditor;
</script>

<style lang="scss" module>
.tags {
  &Editor {
    display: flex;
    justify-content: space-between;

  }
  &Form {
    width: 400px;
    margin-left: 20px;
    flex: none;
  }

  &Wrapper {
    margin: -10px -10px 0 0;

    .tag {
      margin: 10px 10px 0 0;
    }
  }
}

</style>
