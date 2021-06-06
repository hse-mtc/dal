<template>
  <el-col
    v-loading="loading"
    :offset="2"
    :span="20"
    class="teacher"
  >
    <el-row class="pageTitle">
      <el-col>
        <div v-if="$route.params.teacherId" class="d-flex align-items-center">
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
    <el-form
      ref="form"
      :model="form"
      :rules="rules"
      label-width="150px"
      :label-position="$route.params.teacherId ? 'left' : 'right'"
      class="form"
    >
      <el-form-item label="Фото">
        <el-upload
          class="avatar-uploader"
          action="https://jsonplaceholder.typicode.com/posts/"
          :show-file-list="false"
          :on-success="handleAvatarSuccess"
          :before-upload="beforeAvatarUpload"
        >
          <img v-if="form.photo" :src="form.photo" class="avatar">
          <i v-else class="el-icon-picture-outline avatar-uploader-icon" />
        </el-upload>
      </el-form-item>

      <el-form-item label="Фамилия" prop="surname">
        <el-input
          v-model="form.surname"
          clearable
          placeholder="Введите фамилию"
        />
      </el-form-item>

      <el-form-item label="Имя" prop="name">
        <el-input v-model="form.name" clearable placeholder="Введите имя" />
      </el-form-item>

      <el-form-item label="Отчество" prop="patronymic">
        <el-input
          v-model="form.patronymic"
          clearable
          placeholder="Введите отчество"
        />
      </el-form-item>

      <el-form-item label="Звание" prop="rank">
        <el-select
          v-model="form.rank"
          value-key="rank"
          placeholder="Выберите звание"
          style="display: block"
        >
          <el-option
            v-for="item in ranks"
            :key="item.rank"
            :label="item.rank"
            :value="item"
          />
        </el-select>
      </el-form-item>

      <el-form-item label="Должность" prop="teacher_post">
        <el-select
          v-model="form.teacher_post"
          value-key="teacher_post"
          placeholder="Выберите должность"
          style="display: block"
        >
          <!-- eslint-disable vue/camelcase -->
          <el-option
            v-for="item in teacher_posts"
            :key="item.teacher_post"
            :label="item.teacher_post"
            :value="item"
          />
        </el-select>
      </el-form-item>

      <el-form-item label="Цикл" prop="milfaculty">
        <el-select
          v-model="form.milfaculty"
          value-key="milfaculty"
          placeholder="Выберите цикл"
          style="display: block"
        >
          <el-option
            v-for="item in milfaculties"
            :key="item.milfaculty"
            :label="item.milfaculty"
            :value="item"
          />
        </el-select>
      </el-form-item>

      <el-form-item
        v-if="form.milfaculty"
        label="Прикрепленный взвод"
        prop="milgroup"
      >
        <el-select
          v-model="form.milgroup"
          value-key="milgroup"
          placeholder="Выберите прикрепленный взвод"
          style="display: block"
        >
          <el-option
            v-for="item in milgroups"
            :key="item.milgroup"
            :label="item.milgroup"
            :value="item"
          >
            <span style="float: left"> {{ item.milgroup }} </span>
            <span style="float: right; color: #8492a6; font-size: 13px">
              {{ item.milfaculty }}
            </span>
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSubmit">
          Сохранить
        </el-button>
      </el-form-item>
    </el-form>
  </el-col>
</template>

<script>
import { patchTeacher, findTeacher } from "@/api/teachers";
import { patchError, patchSuccess, getError } from "@/utils/message";
import {
  getMilFaculties,
  getMilGroups,
  getPosts,
  getRanks,
} from "@/api/reference-book";

export default {
  name: "Teacher",
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
        rank: "",
        teacher_post: "",
        milfaculty: "",
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
        rank: [
          {
            required: true,
            message: "Пожалуйста, выберите звание",
            trigger: "change",
          },
        ],
        teacher_post: [
          {
            required: true,
            message: "Пожалуйста, выберите должность",
            trigger: "change",
          },
        ],
        milfaculty: [
          {
            required: true,
            message: "Пожалуйста, выберите цикл",
            trigger: "change",
          },
        ],
      },
      milgroups: [],
      milfaculties: [],
      ranks: [],
      teacher_posts: [],
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
      this.milfaculties = (await getMilFaculties()).data;
      this.ranks = (await getRanks()).data;
      this.teacher_posts = (await getPosts()).data;
      const id = this.$route.params.teacherId;
      if (id) {
        try {
          this.loading = true;
          this.form = (await findTeacher(id)).data;
        } catch {
          getError("преподавтеля");
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
          this.form.milgroup = this.form.milgroup
            ? this.form.milgroup.milgroup
            : null;
          try {
            await patchTeacher(this.form);
            patchSuccess("преподавателя");
          } catch (err) {
            patchError("преподавателя", err.response.status);
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
@import "style.scss";
</style>
