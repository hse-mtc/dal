<template>
  <div v-if="subjects.length !== 0" class="subjects">
    <div class="subjects-title">
      Мои предметы
    </div>
    <div :id="subjects[0].id" class="subjects-content active" @click="selectSubject($event)">{{ subjects[0].title }}</div>
    <div
      v-for="item in subjects.slice(1)"
      :id="item.id"
      :key="item.id"
      class="subjects-content"
      @click="selectSubject($event)"
    >
      {{ item.title }}
    </div>
  </div>
</template>

<script>
import { getSubjects } from '@/api/subjects'

export default {
  name: '',
  components: {},
  data() {
    return {
      subjects: []
    }
  },
  created() {
    getSubjects().then(response => {
      this.subjects = response.data
      this.$router.replace({ name: 'Teaching Materials', query: { 'subject': this.subjects[0].id }})
    }).catch(() => {
      console.log('Данные по предметам не указаны')
    })
  },
  mounted() {
  },
  methods: {
    selectSubject(event) {
      document.querySelectorAll('.subjects-content').forEach(item => {
        item.classList.remove('active')
      })
      event.target.classList.add('active')
      console.log(event.target.id)
      this.$router.replace({ name: 'Teaching Materials', query: { 'subject': event.target.id }})
    }
  }
}

</script>

<style scoped lang="scss">
  @import "style";
</style>
