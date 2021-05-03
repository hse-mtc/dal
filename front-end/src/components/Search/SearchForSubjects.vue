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
export default {
  name: "",
  components: {},
  props: {
    placeholder: {
      type: String,
      default: "",
    },
  },
  mounted() {
    const query = this.$route.query.subjectsSearch;
    this.$refs.searchInput.value = query || "";
  },
  methods: {
    search() {
      this.$router.push({
        query: {
          subjectsSearch: this.$refs.searchInput.value,
        },
      });
    },
    deleteText() {
      this.$refs.searchInput.value = "";
      this.$router.push({
        query: {
          subjectsSearch: "",
        },
      });
    },
  },
};
</script>

<style scoped lang="scss">
@import "style";
</style>
