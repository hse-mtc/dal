<template>
  <div class="mysearch d-flex">
    <input
        ref="searchInput"
        type="text"
        class="words-search"
        :placeholder="placeholder"
    />
    <img
        src="@/assets/delete-cross.svg"
        class="delete-cross"
        alt=""
        @click="deleteHandler"
    />
    <img
        src="@/assets/scienceWorks/searchIcon.svg"
        class="search-icon"
        @click="search"
    />
  </div>
</template>

<script>
export default {
  name: "SearchBar",
  components: {},
  props: {
    placeholder: {
      type: String,
      default: 'Введите текст'
    },
    delete: {
      type: Function,
    },
    search: {
      type: Function,
      required: true
    }
  },
  methods: {
    deleteHandler() {
      this.$refs.searchInput.value = "";
      if (this.delete) { this.delete() }
    },
  },
}
</script>

<style scoped lang="scss">
.mysearch {
  border-bottom: 1px solid #a7a7ab;
  align-items: center;
  .words-search {
    width: 100%;
    background-color: inherit;
    border: none;
    padding-bottom: 10px;
    &:focus {
      outline: none;
    }
  }
  .search-icon {
    cursor: pointer;
    width: 35px;
    height: 35px;
    margin-bottom: 10px;
  }
  .delete-cross {
    display: none;
    cursor: pointer;
    width: 15px;
    height: 15px;
    margin-bottom: 10px;
    margin-right: 10px;
  }
  &:hover {
    .delete-cross {
      display: flex;
    }
  }
}

</style>
