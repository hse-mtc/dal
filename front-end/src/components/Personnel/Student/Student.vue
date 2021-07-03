<template>
  <el-col :offset="2" :span="20" class="student-page">
    <el-row class="pageTitle">
      <el-col>
        <div v-if="$route.params.studentId" class="d-flex align-items-center">
          <img
            src="@/assets/scienceWorks/previous.svg"
            style="position: absolute; left: -40px; cursor: pointer"
            height="22px"
            alt="назад"
            @click="backToPersonnel"
          >
          Студент
        </div>
      </el-col>
    </el-row>
    <div class="row">
      <StudentGeneral />
    </div>
    <div class="row">
      <div class="column">
        <StudentDiscipline />
        <StudentExtra />
      </div>
      <div class="column">
        <StudentAchievements />
        <StudentPerformance />
      </div>
    </div>
  </el-col>
</template>

<script>
import StudentGeneral from "@/components/Personnel/Student/StudentGeneral/StudentGeneral.vue";
import StudentExtra from "@/components/Personnel/Student/StudentExtra/StudentExtra.vue";
import StudentAchievements from "@/components/Personnel/Student/StudentAchievements/StudentAchievements.vue";
import StudentDiscipline from "@/components/Personnel/Student/StudentDiscipline/StudentDiscipline.vue";
import StudentPerformance from "@/components/Personnel/Student/StudentPerformance/StudentPerformance.vue";

export default {
  name: "Student",
  components: {
    StudentGeneral,
    StudentExtra,
    StudentAchievements,
    StudentDiscipline,
    StudentPerformance,
  },
  methods: {
    backToPersonnel() {
      this.$router.push("Personnel");
    },
  },
};
</script>

<style scoped lang="scss">
@import "style";
</style>
