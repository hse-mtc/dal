<template>
  <ExpandBox title="Умения и достижения" @toggled="toggled">
    Student Achivements
  </ExpandBox>
</template>

<script>
import ExpandBox from "@/components/ExpandBox/ExpandBox.vue";

export default {
  name: "StudentAchievements",
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
