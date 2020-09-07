<template>
  <div class="app-container">
    <Materials />
  </div>
</template>

<script>
import Materials from '../../components/Materials/Materials'

export default {
  components: {
    Materials
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
