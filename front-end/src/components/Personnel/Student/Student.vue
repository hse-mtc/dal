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
        <el-input
          v-model="form.name"
          clearable
          placeholder="Введите имя"
        />
      </el-form-item>

      <el-form-item label="Отчество" prop="patronymic">
        <el-input
          v-model="form.patronymic"
          clearable
          placeholder="Введите отчество"
        />
      </el-form-item>

      <el-form-item label="Взвод" prop="milgroup">
        <el-select
          v-model="form.milgroup"
          value-key="milgroup"
          placeholder="Выберите взвод"
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
          Отправить
        </el-button>
      </el-form-item>
    </el-form>
  </el-drawer>
</template>

<script>
import { patchStudent } from "@/api/students";
import { patchError, patchSuccess } from "@/utils/message";
import { getMilGroups } from "@/api/reference-book";

export default {
  name: "Student",
  model: {
    prop: "show",
    event: "show-change",
  },
  props: {
    student: {
      type: Object,
      required: true,
    },
    show: {
      type: Object,
      required: true,
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
    modal: {
      get() {
        return this.show;
      },
      set(value) {
        this.$emit("show-change", value);
      },
    },
  },
  watch: {
    async student(value) {
      Object.keys(this.form).forEach(key => {
        this.form[key] = value[key];
      });
      await this.fetchData();
    },
  },
  methods: {
    async fetchData() {
      this.milgroups = (await getMilGroups()).data;
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
