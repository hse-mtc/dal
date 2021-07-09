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
        <el-button type="primary" @click="dialog = true">
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
    <el-dialog
      width="500px"
      :visible.sync="dialog"
      destroy-on-close
      :close-on-click-modal="false"
      :before-close="beforeClose"
    >
      <ChangePasswordForm in-dialog @submited="dialog = false" />
    </el-dialog>
  </el-col>
</template>

<script>
import StudentGeneral from "@/components/Personnel/Student/StudentGeneral/StudentGeneral.vue";
import StudentExtra from "@/components/Personnel/Student/StudentExtra/StudentExtra.vue";
import StudentAchievements from "@/components/Personnel/Student/StudentAchievements/StudentAchievements.vue";
import StudentDiscipline from "@/components/Personnel/Student/StudentDiscipline/StudentDiscipline.vue";
import StudentPerformance from "@/components/Personnel/Student/StudentPerformance/StudentPerformance.vue";
import { UserModule } from "@/store";
import ChangePasswordForm from "@/components/ChangePasswordForm/ChangePasswordForm.vue";

export default {
  name: "Student",
  components: {
    StudentGeneral,
    StudentExtra,
    StudentAchievements,
    StudentDiscipline,
    StudentPerformance,
    ChangePasswordForm,
  },
  data() {
    return {
      dialog: false,
    };
  },
  computed: {
    personType() {
      return UserModule.personType;
    },
    personId() {
      return UserModule.personId;
    },
    id() {
      return this.$route.params.studentId;
    },
    isProfile() {
      return this.personType === "student" && this.personId === +this.id;
    },
  },
  methods: {
    backToPersonnel() {
      this.$router.push({ name: "Personnel" });
    },
    async beforeClose() {
      try {
        await this.$confirm(
          "Вы уверены, что хотите закрыть окно смены пароля?",
          "Подтверждение",
          {
            confirmButtonText: "Да",
            cancelButtonText: "Отмена",
            type: "warning",
          },
        );
        this.dialog = false;
      } catch {}
    },
  },
};
</script>

<style scoped lang="scss">
@import "style";
</style>
