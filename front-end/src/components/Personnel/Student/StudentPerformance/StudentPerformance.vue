<template>
  <ExpandBox title="Успеваемость" @toggled="toggled">
    Student Performance
  </ExpandBox>
</template>

<script>
import ExpandBox from "@/components/ExpandBox/ExpandBox.vue";

export default {
  name: "StudentPerformance",
  components: { ExpandBox },
  data() {
    return {};
  },
  methods: {
    fetchData() {},
    toggled(expanded) {
      if (expanded) {
        this.fetchData();
      }
    },
  },
};
</script>

<style lang="scss" scoped>
@import "style";
</style>
