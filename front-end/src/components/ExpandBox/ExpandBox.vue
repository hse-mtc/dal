<template>
  <div class="expand-box" :class="{ expanded: expanded, 'no-expand': noExpand }">
    <div class="header" @click="toggle">
      <span class="title">{{ title }}</span>
      <SvgIcon v-if="!noExpand" icon-class="chevron-down" class="icon" />
    </div>
    <transition name="expand">
      <div v-show="expanded" class="body">
        <slot />
      </div>
    </transition>
  </div>
</template>

<script>
export default {
  name: "ExpandBox",
  props: {
    title: { type: String, required: true },
    noExpand: { type: Boolean, default: false },
  },
  data() {
    return {
      expanded: this.noExpand,
    };
  },
  methods: {
    toggle() {
      if (!this.noExpand) {
        this.expanded = !this.expanded;
        this.$emit("toggled", this.expanded);
      }
    },
  },
};
</script>

<style lang="scss" scoped>
@import "style";
</style>
