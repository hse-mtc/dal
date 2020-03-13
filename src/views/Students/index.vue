<template>
  <div class="app-container">
    <Students />
  </div>
</template>

<script>
import Students from '../../components/Students/Students'

export default {
  components: {
    Students
  },
  data() {
    return {
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    fetchData() {
    }
  }
}
</script>