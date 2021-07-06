<template>
  <div class="expand-box" :class="{ expanded: expanded, 'non-expandable': nonExpandable }">
    <div class="header" @click="toggle">
      <span class="title">{{ title }}</span>
      <SvgIcon v-if="!nonExpandable" icon-class="chevron-down" class="icon" />
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
    nonExpandable: { type: Boolean, default: false },
  },
  data() {
    return {
      expanded: this.nonExpandable,
    };
  },
  methods: {
    toggle() {
      if (!this.nonExpandable) {
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
