<template>
  <div class="app-container">
    <Marks />
  </div>
</template>

<script>
import Marks from "../../components/Marks/Marks";

export default {
  components: {
    Marks,
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
