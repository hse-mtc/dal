<template>
  <div class="mysearch d-flex">
    <input
      ref="searchInput"
      type="text"
      class="words-search"
      :placeholder="placeholder"
      @keyup.enter="search"
    >
    <img
      src="../../assets/delete-cross.svg"
      class="delete-cross"
      alt=""
      @click="deleteText"
    >
    <img
      src="../../assets/scienceWorks/searchIcon.svg"
      class="search-icon"
      @click="search"
    >
  </div>
</template>

<script>
import _omit from "lodash/omit";

export default {
  name: "",
  components: {},
  props: {
    placeholder: {
      type: String,
      default: "",
    },
  },
  methods: {
    search() {
      this.$router.push({
        query: {
          search: this.$refs.searchInput.value,
          ...this.$route.query,
        },
      });
    },
    deleteText() {
      this.$refs.searchInput.value = "";
      this.$router.push({
        query: _omit(this.$route.query, ["search"]),
      });
    },
  },
};
</script>

<style scoped lang="scss">
@import "style";
</style>
