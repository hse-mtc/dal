<template>
  <el-row v-if="subjects.length !== 0" class="subjects mt-5">
    <el-col :span="8" v-for="(item, index) in subjects" :key="subjects.id" class="subjects-wrapper mt-5">
      <el-col>
        <div class="subjects-card" :id="item.id" v-bind:class="{ 'm-0': ++index % 3 === 0 }" @click="selectSubject">{{item.title}}</div>
      </el-col>
    </el-col>
  </el-row>
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
    if (this.$store.getters.subjects.length === 0) {
      getSubjects().then(response => {
        this.subjects = response.data
        this.$store.dispatch('projectData/addSubjects', this.subjects);
        this.$router.replace({ name: 'Teaching Materials'})
      }).catch(() => {
        // eslint-disable-next-line no-console
        console.log('Данные по предметам не указаны')
      })
    } else {
      this.subjects = this.$store.getters.subjects
    }

  },
  mounted() {
  },
  methods: {
    selectSubject(event) {
      // eslint-disable-next-line no-console
      this.$router.push({
        query: {
          subjectId: event.target.id
        }
      })
    }
  }
}

</script>

<style scoped lang="scss">
  @import "style";
</style>
