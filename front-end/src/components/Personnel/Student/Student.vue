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
        {{ isProfile ? "Мой профиль" : fullname }}
      </div>
      <div v-if="isProfile">
        <el-button type="primary" @click="dialog = true">
          Сменить пароль
        </el-button>
      </div>
    </div>
    <div class="row">
      <StudentGeneral :milgroup="milgroup" />
    </div>
    <div class="row">
      <StudentExtra :milgroup="milgroup" />
    </div>
    <div class="row">
      <div class="column">
        <StudentPerformance />
        <StudentDiscipline />
      </div>
      <div class="column">
        <StudentAchievements :milgroup="milgroup" />
        <StudentNotes v-if="personType !== 'student'" />
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
import StudentNotes from "@/components/Personnel/Student/StudentNotes/StudentNotes.vue";
import { UserModule } from "@/store";
import ChangePasswordForm from "@/components/ChangePasswordForm/ChangePasswordForm.vue";
import { findStudent } from "@/api/students";

export default {
  name: "Student",
  components: {
    StudentGeneral,
    StudentExtra,
    StudentAchievements,
    StudentDiscipline,
    StudentPerformance,
    StudentNotes,
    ChangePasswordForm,
  },
  data() {
    return {
      dialog: false,
      student: {},
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
    fullname() {
      return this.student.fullname;
    },
    milgroup() {
      return this.student.milgroup;
    },
  },
  async created() {
    this.student = (await findStudent(this.id)).data;
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
