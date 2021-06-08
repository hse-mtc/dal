<template>
  <ExpandBox title="Дополнительная информация" @toggled="toggled">
    Student Extra
  </ExpandBox>
</template>

<script>
import ExpandBox from "@/components/ExpandBox/ExpandBox.vue";

export default {
  name: "StudentExtra",
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
