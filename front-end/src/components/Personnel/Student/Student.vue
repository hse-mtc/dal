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
          {{ fullname }}
        </div>
      </el-col>
    </el-row>
    <div class="row">
      <StudentGeneral />
    </div>
    <div class="row">
      <div class="column">
        <StudentExtra />
        <StudentDiscipline />
      </div>
      <div class="column">
        <StudentAchievements />
        <StudentPerformance />
      </div>
    </div>
  </el-col>
</template>

<script>
import { patchStudent, findStudent } from "@/api/students";
import { patchError, patchSuccess, getError } from "@/utils/message";
import { getMilGroups } from "@/api/reference-book";
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
  data() {
    return {
      loading: false,
      form: {
        id: 0,
        milgroup: null,
        surname: "",
        name: "",
        patronymic: "",
        photo: null,
      },
      rules: {
        surname: [
          {
            required: true,
            message: "Пожалуйста, введите фамилию",
            trigger: "blur",
          },
        ],
        name: [
          {
            required: true,
            message: "Пожалуйста, введите имя",
            trigger: "blur",
          },
        ],
        milgroup: [
          {
            required: true,
            message: "Пожалуйста, выберите взвод",
            trigger: "change",
          },
        ],
      },
      milgroups: [],
      statuses: ["Обучается", "Отчислен", "Завершил"],
    };
  },
  computed: {
    fullname() {
      return this.form.fullname;
    },
  },
  async created() {
    await this.fetchData();
  },
  methods: {
    async fetchData() {
      this.milgroups = (await getMilGroups()).data;
      const id = this.$route.params.studentId;
      if (id) {
        try {
          this.loading = true;
          this.form = (await findStudent(id)).data;
        } catch {
          getError("студента");
        } finally {
          this.loading = false;
        }
      }
    },
    handleAvatarSuccess(res, file) {
      this.form.foto = URL.createObjectURL(file.raw);
    },
    beforeAvatarUpload(file) {
      const isValidType = file.type === "image/jpeg" || file.type === "image/png";
      const isLt2M = file.size / 1024 / 1024 < 2;

      if (!isValidType) {
        this.$message.error("Изображение должно иметь формат jpeg или png.");
      }
      if (!isLt2M) {
        this.$message.error("Размер изображения не должен превышать 2 МБ.");
      }
      return isValidType && isLt2M;
    },
    onSubmit() {
      this.$refs.form.validate(async valid => {
        if (valid) {
          this.form.milgroup = this.form.milgroup.milgroup;
          try {
            await patchStudent(this.form);
            patchSuccess("студента");
          } catch (err) {
            patchError("студента", err.response.status);
          }
        }
      });
    },
    backToPersonnel() {
      this.$router.push({ path: "/personnel/" });
    },
  },
};
</script>

<style scoped lang="scss">
@import "style";
</style>
