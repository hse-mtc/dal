<template>
  <div class="root">
    <PageHeader title="Библиотека" button="+ Добавить учебник" :click="addNewBook"/>
    <SearchBar placeholder="Введите название книги" :search="searchBook" :delete="deleteSearchInput" />

  </div>
</template>

<script>
import PageHeader from "@/common/PageHeader";
import SearchBar from "@/common/SearchBar";
export default {
  name: "Library",
  components: {
    SearchBar,
    PageHeader
  },
  methods: {
    addNewBook() {
      console.log('addNewBook func')
    },
    searchBook() {
      console.log('searchBook func')
    },
    deleteSearchInput() {
      console.log('deleteSearchInput func')
    }
  }
}
</script>

<style scoped lang="scss">
.root {

}
</style>
