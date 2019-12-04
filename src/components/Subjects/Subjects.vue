<template>
  <el-row v-if="subjects.length !== 0" class="subjects mt-5">
    <el-col :span="8" v-for="(item, index) in subjects" :key="subjects.id" class="subjects-wrapper mt-5">
      <el-col>
        <div class="subjects-card" v-bind:class="{ 'm-0': ++index % 3 === 0 }">{{item.title}}</div>
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
    getSubjects().then(response => {
      this.subjects = response.data
      this.$router.replace({ name: 'Teaching Materials'})
    }).catch(() => {
      console.log('Данные по предметам не указаны')
    })
  },
  mounted() {
  },
  methods: {
    selectSubject(event) {

    }
  }
}

</script>

<style scoped lang="scss">
  @import "style";
</style>
