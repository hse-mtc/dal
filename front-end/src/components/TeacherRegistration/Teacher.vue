<template>
  <div>
    <ElForm
      ref="form"
      :model="teacher"
      :rules="rules"
      auto-complete="on"
      label-position="left"
    >
      <div class="field-title">
        Корпоративная почта ВШЭ
      </div>
      <ElFormItem prop="contact_info.corporate_email">
        <ElInput
          v-model.trim="teacher.contact_info.corporate_email"
          placeholder="Укажите корпоративную почту"
          type="text"
          tabindex="1"
          auto-complete="on"
        />
      </ElFormItem>

      <div class="field-title">
        Фамилия
      </div>
      <ElFormItem prop="surname">
        <ElInput
          ref="surname"
          v-model="teacher.surname"
          placeholder="Укажите фамилию"
          name="lastName"
          type="text"
          tabindex="1"
          auto-complete="on"
        />
      </ElFormItem>

      <div class="" style="display: flex">
        <div style="width: 45%">
          <div class="field-title">
            Имя
          </div>
          <ElFormItem prop="name">
            <ElInput
              ref="name"
              v-model="teacher.name"
              placeholder="Укажите имя"
              name="name"
              type="text"
              tabindex="1"
              auto-complete="on"
            />
          </ElFormItem>
        </div>

        <div style="margin-left: 63px; width: 45%">
          <div class="field-title">
            Отчество
          </div>
          <ElFormItem prop="patronymic">
            <ElInput
              ref="patronymic"
              v-model="teacher.patronymic"
              placeholder="Укажите отчество"
              name="patronymic"
              type="text"
              tabindex="1"
              auto-complete="on"
            />
          </ElFormItem>
        </div>
      </div>

      <div class="field-title">
        Цикл
      </div>
      <ElFormItem prop="milfaculty">
        <ElSelect
          v-model="teacher.milfaculty"
          placeholder="Выберите цикл"
          style="display: block"
        >
          <ElOption
            v-for="milfaculty in milfaculties"
            :key="milfaculty.id"
            :label="milfaculty.title"
            :value="milfaculty.id"
          />
        </ElSelect>
      </ElFormItem>

      <div class="field-title">
        Прикреплённые взвода
      </div>
      <ElFormItem prop="milgroups">
        <ElSelect
          v-model="teacher.milgroups"
          placeholder="Выберите прикреплённые взвода"
          style="display: block"
          multiple
        >
          <ElOption
            v-for="milgroup in milgroups"
            :key="milgroup.id"
            :label="milgroup.title"
            :value="milgroup.id"
          >
            <span style="float: left">
              {{ milgroup.title }}
            </span>
            <span style="float: right; color: #8492a6; font-size: 13px; margin-right: 15px;">
              {{ milgroup.milfaculty.abbreviation }}
            </span>
          </ElOption>
        </ElSelect>
      </ElFormItem>

      <div class="field-title">
        Звание
      </div>
      <ElFormItem prop="rank">
        <ElSelect
          v-model="teacher.rank"
          placeholder="Выберите звание"
          style="display: block"
        >
          <ElOption
            v-for="rank in teacherRanks"
            :key="rank.value"
            :label="rank.label"
            :value="rank.value"
          />
        </ElSelect>
      </ElFormItem>

      <div class="field-title">
        Должность
      </div>
      <ElFormItem prop="post">
        <ElSelect
          v-model="teacher.post"
          placeholder="Выберите должность"
          style="display: block"
        >
          <ElOption
            v-for="post in teacherPosts"
            :key="post.value"
            :label="post.label"
            :value="post.value"
          />
        </ElSelect>
      </ElFormItem>

      <ElButton
        :loading="loading"
        type="primary"
        style="width: 190px; margin-bottom: 30px; margin-top: 20px"
        @click.native.prevent="registerTeacher"
      >
        Зарегистрироваться
      </ElButton>
    </ElForm>
  </div>
</template>

<script>
import { ReferenceModule } from "@/store";

import { TeacherRanksMixin, TeacherPostsMixin } from "@/mixins/teachers";
import { validCorEmail } from "@/utils/validate";
import { postError, downloadError } from "@/utils/message";
import { registerTeacher } from "@/api/user";

export default {
  mixins: [TeacherRanksMixin, TeacherPostsMixin],

  data() {
    const requiredRule = {
      required: true,
      message: "Обязательное поле",
      trigger: "blur",
    };

    const validateEmail = (rule, value, callback) => {
      if (!validCorEmail(value)) {
        callback(new Error("Пожалуйста, введите корректный email"));
      } else {
        callback();
      }
    };
    const emailRule = {
      required: true,
      trigger: "blur",
      validator: validateEmail,
    };

    return {
      awaitingResponse: false,

      teacher: {
        surname: "",
        name: "",
        patronymic: "",
        milfaculty: null,
        milgroups: [],
        post: "",
        rank: "",
        contact_info: {
          corporate_email: "",
        },
      },

      rules: {
        surname: [requiredRule],
        name: [requiredRule],
        milfaculty: [requiredRule],
        post: [requiredRule],
        rank: [requiredRule],
        "contact_info.corporate_email": [emailRule],
      },
    };
  },

  computed: {
    loading() {
      return this.awaitingResponse || this.teacherRanksAreLoading || this.teacherPostsAreLoading;
    },

    milfaculties() {
      return ReferenceModule.milfaculties;
    },
    milgroups() {
      return ReferenceModule.milgroups;
    },
  },

  async created() {
    this.awaitingResponse = true;

    const responses = [];

    /* eslint-disable no-underscore-dangle */
    if (!ReferenceModule._milfacultiesLoaded) {
      responses.push(ReferenceModule.fetchMilfaculties());
    }
    if (!ReferenceModule._milgroupsLoaded) {
      responses.push(ReferenceModule.fetchMilgroups());
    }
    /* eslint-enable no-underscore-dangle */

    try {
      await Promise.all(responses);
    } catch (e) {
      downloadError("данныe о циклах и взводах", e.response?.status);
    } finally {
      this.awaitingResponse = false;
    }
  },

  methods: {
    async registerTeacher() {
      const isDataValid = await this.$refs.form.validate();
      if (!isDataValid) {
        return;
      }

      this.awaitingResponse = true;

      try {
        await registerTeacher(this.teacher);
        this.$emit("registration-completed");
      } catch (e) {
        if (e.response.data) {
          if (e.response.data.error_message === "email_already_exists") {
            this.$message.error("Аккаунт с такой электронной почтой уже существует");
          } else {
            postError("преподавателя", e.response?.status);
          }
        }
      } finally {
        this.awaitingResponse = false;
      }
    },
  },
};
</script>

<style scoped lang="scss">
@import "style";
</style>
