<template>
  <el-drawer :visible.sync="modal" direction="rtl" size="40%" :destroy-on-close="true">
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
      <el-form-item
        label="Образовательная программа"
        prop="university_info.program"
      >
        <el-select
          v-model="form.university_info.program"
          value-key="code"
          placeholder="Выберите программу"
          style="display: block"
        >
          <el-option
            v-for="item in programs"
            :key="item.code"
            :label="item.program"
            :value="item"
          >
            <span style="float: left">{{ item.program }}</span>
            <span style="float: right; color: #8492a6; font-size: 13px">{{
              item.code
            }}</span>
          </el-option>
        </el-select>
      </el-form-item>

      <el-form-item label="Дата рождения" prop="birth_info.date">
        <el-date-picker
          v-model="form.birth_info.date"
          type="date"
          placeholder="Выберите дату рождения"
          format="DD.MM.yyyy"
          value-format="yyyy-MM-DD"
        >
        </el-date-picker>
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="onSubmit">Отправить</el-button>
      </el-form-item>
    </el-form>
  </el-drawer>
</template>

<script>
import { patchStudent } from "@/api/students";
import { patchError, patchSuccess } from "@/utils/message";

export default {
  name: "Student",
  props: ["student", "show"],
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
        milgroup: {},
        university_info: {},
        birth_info: "",
        surname: "",
        name: "",
        patronymic: "",
        photo: null,
        status: "",
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
        university_info: {
          program: [
            {
              required: true,
              message: "Пожалуйста, выберите обр. программу",
              trigger: "change",
            },
          ],
        },
        birth_info: {
          birthdate: [
            {
              type: "string",
              required: true,
              message: "Пожалуйста, выберите дату рождения",
              trigger: "change",
            },
          ],
        },
      },
      milgroups: [
        { milgroup: 1807, milfaculty: "ВКС", weekday: 4 },
        { milgroup: 1808, milfaculty: "ВКС", weekday: 4 },
        { milgroup: 1809, milfaculty: "ВКС", weekday: 4 },
        { milgroup: 1810, milfaculty: "РВСН", weekday: 4 },
      ],
      programs: [
        {
          program: "Информатика и вычислительная техника",
          code: "09.03.01",
        },
        { program: "Программная инженерия", code: "09.03.04" },
        { program: "Машиностроение", code: "15.03.01" },
      ],
      statuses: ["Обучается", "Отчислен", "Завершил"],
    };
  },
  watch: {
    student(value) {
      this.form = value;
    },
  },
  methods: {
    handleAvatarSuccess(res, file) {
      this.form.foto = URL.createObjectURL(file.raw);
    },
    beforeAvatarUpload(file) {
      const isJPG = file.type === "image/jpeg";
      const isLt2M = file.size / 1024 / 1024 < 2;

      if (!isJPG) {
        this.$message.error("Изображение должно быть формата JPG.");
      }
      if (!isLt2M) {
        this.$message.error("Размер изображения не должен превышать 2 МБ.");
      }
      return isJPG && isLt2M;
    },
    onSubmit() {
      this.$refs["form"].validate(async (valid) => {
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
      console.log('zhopa');
      this.$emit("closeModal");
    },
  },
};
</script>

<style scoped lang="scss">
@import "style.scss";
</style>
