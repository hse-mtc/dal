<template>
  <div class="mysearch d-flex">
    <input type="text" class="words-search" :placeholder="placeholder">
    <img src="../../assets/scienceWorks/searchIcon.svg" class="search-icon">
  </div>
</template>

<script>
export default {
  name: '',
  components: {},
  props: ["placeholder"],
  methods: {

  }
}

</script>

<style scoped lang="scss">
  @import "style";
</style>
