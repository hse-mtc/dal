<template>
  <div
    class="cta"
    :style="{border: border, color: color, background: background}"
    @click="onClick"
  >
    <slot />
  </div>
</template>

<script>
export default {
  name: "CtaButton",
  props: {
    background: {
      type: String,
      default: "#0061D9",
    },
    color: {
      type: String,
      default: "#fff",
    },
    border: {
      type: String,
      default: "none",
    },
  },
  methods: {
    onClick() {
      this.$emit("click");
    },
  },
};
</script>

<style scoped lang="scss">
@import "@/styles/variables.scss";

.cta {
  color: white;
  width: max-content;
  border-radius: $xs;
  padding: 16px 24px !important;
  cursor: pointer;
}
</style>
