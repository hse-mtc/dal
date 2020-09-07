<template>
  <div class="mysearch d-flex">
    <input ref="searchInput" type="text" class="words-search" :placeholder="placeholder">
    <img src="../../assets/delete-cross.svg" class="delete-cross" alt="" @click="deleteText">
    <img src="../../assets/scienceWorks/searchIcon.svg" class="search-icon" @click="search">
  </div>
</template>

<script>
export default {
  name: '',
  components: {},
  props: ["placeholder"],
  methods: {
    search() {
      this.$router.push({
        query: {
          subjectId: this.$route.query.subjectId,
          materialsSearch: this.$refs.searchInput.value,
        }
      })
    },
    deleteText() {
      this.$refs.searchInput.value = ''
      this.$router.push({
        query: {
          subjectId: this.$route.query.subjectId,
          materialsSearch: ''
        }
      })
    }
  }
}

</script>

<style scoped lang="scss">
  @import "style";
</style>
