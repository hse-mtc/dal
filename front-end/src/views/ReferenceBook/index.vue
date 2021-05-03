<template>
  <div class="app-container">
    <ReferenceBook />
  </div>
</template>

<script>
import ReferenceBook from "../../components/ReferenceBook/ReferenceBook.vue";

export default {
  components: {
    ReferenceBook,
  },
  data() {
    return {};
  },
  created() {
    this.fetchData();
  },
  methods: {
    fetchData() {},
  },
};
</script>
