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
    @change="change"
  />
</template>

<script>
import { Component, Emit, Prop } from "vue-property-decorator";
import Select from "./Select.vue";
import InputsMixin from "./inputsMixin";

@Component({
  name: "TagsInput",
  components: { Select },
})
class TagsInput extends InputsMixin {
  @Prop({ type: Array, default: () => [] }) tags

  tag = ""

  @Emit()
  change(values) {
    console.log("values", values);
    return values
      .map(item => item.trim().toLowerCase())
      .filter(item => Boolean(item));
  }
}

export default TagsInput;
</script>
