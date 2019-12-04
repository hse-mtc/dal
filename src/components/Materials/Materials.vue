<template>
  <el-col :offset="2" :span="20" class="scienceWork">
    <el-row class="pageTitle">
      <el-col>
        Учебно-методические материалы
      </el-col>
    </el-row>
    <el-row class="search ">
      <el-col :span="23">
        <Search placeholder="Введите название темы или документа" />
        <Subjects />
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

    }
  },
  created() {
  },
  methods: {
  }
}
</script>

<style scoped lang="scss">
  @import "style";
</style>
