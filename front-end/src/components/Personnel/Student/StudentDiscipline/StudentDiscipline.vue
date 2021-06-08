<template>
  <ExpandBox title="Дисциплина" @toggled="toggled">
    Student Discipline
  </ExpandBox>
</template>

<script>
import ExpandBox from "@/components/ExpandBox/ExpandBox.vue";

export default {
  name: "StudentDiscipline",
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
