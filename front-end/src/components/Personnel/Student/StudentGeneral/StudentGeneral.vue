<template>
  <ExpandBox title="О студенте" no-expand>
    Student General
  </ExpandBox>
</template>

<script>
import ExpandBox from "@/components/ExpandBox/ExpandBox.vue";

export default {
  name: "StudentGeneral",
  components: { ExpandBox },
  data() {
    return {};
  },
  methods: {
    fetchData() {},
  },
};
</script>

<style lang="scss" scoped>
@import "style";
</style>
