<template>
  <div class="app-container">
    <Absence />
  </div>
</template>

<script>
import Absence from "../../components/Absence/Absence.vue";

export default {
  components: {
    Absence,
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
