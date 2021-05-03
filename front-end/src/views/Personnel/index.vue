<template>
  <div class="app-container">
    <Students />
  </div>
</template>

<script>
import Students from "../../components/Personnel/Personnel.vue";

export default {
  components: {
    Students,
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
