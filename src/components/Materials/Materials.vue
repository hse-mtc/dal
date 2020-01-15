<template>
  <el-col :offset="2" :span="20" class="scienceWork">
    <el-row class="pageTitle">
      <el-col>
        <div class="d-flex align-items-center">
          <img src="../../assets/scienceWorks/previous.svg" v-if="subjectId !== undefined" @click="backToSubjects" style="position: absolute; left: -30px; cursor: pointer" height="22px" alt="назад">
          {{subject}}
        </div>
      </el-col>
    </el-row>
    <el-row class="search ">
      <el-col :span="23">
        <Search placeholder="Введите название темы или документа" />
        <Subjects v-if="subjectId === undefined" />
      </el-col>
    </el-row>
  </el-col>
</template>

<script>
import Search from '../Search/Search'
import Subjects from '../Subjects/Subjects'
import SubjectFiles from '../SubjectFiles/SubjectFiles'

export default {
  name: '',
  components: {
    Search,
    Subjects,
    SubjectFiles
  },
  data() {
    return {
      subject: "Учебно-методические материалы",
      subjectId: undefined
    }
  },
  created() {
  },
  methods: {
    setSubject(subjectId) {
      this.subjectId = subjectId
    },
    backToSubjects() {
      this.$router.push({
        query: {
          subjectId: undefined
        }
      })
    }
  },
  watch: {
    '$route'(to, from) {
      this.setSubject(this.$route.query.subjectId)
    }
  },
}
</script>

<style scoped lang="scss">
  @import "style";
</style>
