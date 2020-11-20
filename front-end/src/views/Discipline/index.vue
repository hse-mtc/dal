<template>
  <div class="app-container">
    <Discipline />
  </div>
</template>

<script>
import Discipline from "../../components/Discipline/Discipline";

export default {
  components: {
    Discipline,
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
