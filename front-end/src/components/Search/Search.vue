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
          text: this.$refs.searchInput.value,
          section: this.$route.query.section,
          place: this.$route.query.place,
          author: this.$route.query.author,
          start_date: this.$route.query.start_date,
          end_date: this.$route.query.end_date,
        }
      })
    },
    deleteText() {
      this.$refs.searchInput.value = ''
      this.$router.push({
        query: {
          section: this.$route.query.section,
          place: this.$route.query.place,
          author: this.$route.query.author,
          start_date: this.$route.query.start_date,
          end_date: this.$route.query.end_date,
        }
      })
    }
  }
}

</script>

<style scoped lang="scss">
  @import "style";
</style>
