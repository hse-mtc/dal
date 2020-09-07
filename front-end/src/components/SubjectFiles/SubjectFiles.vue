<template>
  <div class="materials mt-5">
    <div>

    </div>
  </div>
</template>

<script>

import moment from 'moment'
import { getEducationalMaterials } from '@/api/educational_materials'


export default {
  name: '',
  components: {},
  filters: {
    moment: function(date) {
      return moment(date).format('DD MMMM YYYY')
    }
  },
  data() {
    return {
    }
  },
  watch: {
    '$route'(to, from) {

    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    fetchData(target) {
      let subject = this.$route.query.subject
      getEducationalMaterials().then(response => {
        this.subjects = response.data
        this.$router.replace({ name: 'Teaching Materials', query: { 'subject':  subject}})
      }).catch(() => {
        console.log('Данные по документам не указаны')
      })
    },
    moment: function() {
      return moment()
    }
  }
}

</script>

<style scoped lang="scss">
  @import "style";
</style>
