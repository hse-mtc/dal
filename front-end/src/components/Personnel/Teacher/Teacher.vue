<template>
  <el-drawer
    :visible.sync="modal"
    direction="rtl"
    size="40%"
    :destroy-on-close="true"
  >
    <el-form
      ref="form"
      :model="form"
      :rules="rules"
      label-width="250px"
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
          <img v-if="form.photo" :src="form.photo" class="avatar" />
          <i v-else class="el-icon-picture-outline avatar-uploader-icon"></i>
        </el-upload>
      </el-form-item>

      <el-form-item label="Фамилия" prop="surname">
        <el-input
          clearable
          v-model="form.surname"
          placeholder="Введите фамилию"
        ></el-input>
      </el-form-item>

      <el-form-item label="Имя" prop="name">
        <el-input
          clearable
          placeholder="Введите имя"
          v-model="form.name"
        ></el-input>
      </el-form-item>

      <el-form-item label="Отчество" prop="patronymic">
        <el-input
          clearable
          v-model="form.patronymic"
          placeholder="Введите отчество"
        ></el-input>
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
        <el-button type="primary" @click="onSubmit">Отправить</el-button>
      </el-form-item>
    </el-form>
  </el-drawer>
</template>

<script>
import { patchTeacher } from "@/api/teachers";
import { patchError, patchSuccess } from "@/utils/message";
import {
  getMilFaculties,
  getMilGroups,
  getPosts,
  getRanks,
} from "@/api/reference-book";

export default {
  name: "Teacher",
  props: ["teacher", "show"],
  model: {
    prop: "show",
    event: "show-change",
  },
  computed: {
    modal: {
      get() {
        return this.show;
      },
      set(value) {
        this.$emit("show-change", value);
      },
    },
  },
  data() {
    return {
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
  watch: {
    async teacher(value) {
      for (var key in this.form) {
        this.form[key] = value[key];
      }
      await this.fetchData();
    },
  },
  methods: {
    async fetchData() {
      this.milgroups = (await getMilGroups()).data;
      this.milfaculties = (await getMilFaculties()).data;
      this.ranks = (await getRanks()).data;
      this.teacher_posts = (await getPosts()).data;
    },
    handleAvatarSuccess(res, file) {
      this.form.foto = URL.createObjectURL(file.raw);
    },
    beforeAvatarUpload(file) {
      const isValidType =
        file.type === "image/jpeg" || file.type === "image/png";
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
      this.$refs["form"].validate(async (valid) => {
        if (valid) {
          this.form.milgroup = this.form.milgroup ? this.form.milgroup.milgroup : null;
          try {
            await patchTeacher(this.form);
            patchSuccess("студента");
            this.$emit("submitModal");
            this.closeModal();
          } catch (err) {
            patchError("студента", err.response.status);
          }
        }
      });
    },
    closeModal() {
      this.$emit("closeModal");
    },
  },
};
</script>

<style scoped lang="scss">
@import "style.scss";
</style>
