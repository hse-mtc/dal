<template>
  <div class="app-container">
    <ScienceWorks />
  </div>
</template>

<script>
import ScienceWorks from "../../components/ScienceWorks/ScienceWorks.vue";

export default {
  components: {
    ScienceWorks,
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
