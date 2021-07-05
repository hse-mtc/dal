<template>
  <el-col :offset="2" :span="20" class="student-page">
    <div class="page-title">
      <div v-if="$route.params.studentId" class="d-flex align-items-center">
        <img
          src="@/assets/scienceWorks/previous.svg"
          style="position: absolute; left: -40px; cursor: pointer"
          height="22px"
          alt="назад"
          @click="backToPersonnel"
        >
        {{ isProfile ? "Мой профиль" : "Студент" }}
      </div>
      <div v-if="isProfile">
        <el-button type="primary">
          Сменить пароль
        </el-button>
      </div>
    </div>
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
import { mapState } from "vuex";

export default {
  name: "Student",
  components: {
    StudentGeneral,
    StudentExtra,
    StudentAchievements,
    StudentDiscipline,
    StudentPerformance,
  },
  computed: {
    ...mapState("user", ["personType", "personId"]),
    id() {
      return this.$route.params.studentId;
    },
    isProfile() {
      return (
        this.personType === "student" && this.personId === parseInt(this.id, 10)
      );
    },
  },
  methods: {
    backToPersonnel() {
      this.$router.push({ name: "Personnel" });
    },
  },
};
</script>

<style scoped lang="scss">
@import "style";
</style>
