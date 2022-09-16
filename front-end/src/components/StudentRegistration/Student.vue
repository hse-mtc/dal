<template>
  <div>
    <ElForm
      ref="form"
      :model="student"
      :rules="rules"
      auto-complete="on"
      label-position="left"
    >
      <div class="field-title">
        Корпоративная почта ВШЭ
      </div>
      <ElFormItem prop="contact_info.corporate_email">
        <ElInput
          v-model.trim="student.contact_info.corporate_email"
          placeholder="Укажите корпоративную почту"
          type="text"
          tabindex="1"
          auto-complete="on"
        />
      </ElFormItem>

      <div class="field-title">
        Номер мобильного телефона
      </div>
      <ElFormItem prop="contact_info.personal_phone_number">
        <ElInput
          v-model.trim="student.contact_info.personal_phone_number"
          placeholder="Укажите номер мобильного телефона"
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
          v-model="student.surname"
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
              v-model="student.name"
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
              v-model="student.patronymic"
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
        Дата рождения
      </div>
      <ElFormItem prop="birth_date">
        <ElInput
              ref="patronymic"
              v-model="student.birth_info.date"
              placeholder="Укажите дату рождения"
              name="patronymic"
              type="date"
              tabindex="1"
              auto-complete="on"
            />
      </ElFormItem>

      <div class="field-title">
        Взвод
      </div>
      <ElFormItem prop="milgroup">
        <ElSelect
          v-model="student.milgroup"
          placeholder="Выберите свой взвод"
          style="display: block"
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
        Должность
      </div>
      <ElFormItem prop="post">
        <ElSelect
          v-model="student.post"
          placeholder="Выберите должность"
          style="display: block"
        >
          <ElOption
            v-for="post in studentPosts"
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
        @click.native.prevent="registerStudent"
      >
        Зарегистрироваться
      </ElButton>
    </ElForm>
  </div>
</template>

<script>
import { ReferenceModule } from "@/store";

import { StudentPostsMixin } from "@/mixins/students";
import { validCorEmail } from "@/utils/validate";
import { postError, downloadError } from "@/utils/message";
import { registerStudent } from "@/api/user";

export default {
  mixins: [StudentPostsMixin],

  data() {
    const requiredRule = {
      required: true,
      message: "Обязательное поле",
      trigger: "blur",
    };

    const getValidator = (regExp, msg) => ({
      validator: (rule, value, cb) => {
        if (value && !regExp.test(value)) {
          cb(new Error(msg));
        } else {
          cb();
        }
      },
    });

    const validateEmail = (rule, value, callback) => {
      if (!validCorEmail(value)) {
        callback(new Error("Пожалуйста, введите корректный email"));
      } else {
        callback();
      }
    };

    const phoneRule = getValidator(
      /^\+?\d{11}$/,
      "Введите корректный номер телефона",
    );

    const emailRule = {
      required: true,
      trigger: "blue",
      validator: validateEmail,
    };

    return {
      awaitingResponse: false,

      student: {
        surname: "",
        name: "",
        patronymic: "",
        milgroup: null,
        post: null,
        contact_info: {
          corporate_email: "",
          personal_phone_number: "",
        },
        birth_info: {
          date: "",
        },
      },

      rules: {
        surname: [requiredRule],
        name: [requiredRule],
        milgroup: [requiredRule],
        rank: [requiredRule],
        "contact_info.personal_phone_number": [phoneRule],
        "contact_info.corporate_email": [emailRule],
        "birth_info.date": [requiredRule],
      },
    };
  },

  computed: {
    loading() {
      return this.awaitingResponse || this.studentPostsAreLoading;
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

    this.studentPosts.PRIVATE_STUDENT = { label:"-", value: null };
  },

  methods: {
    async registerStudent() {
      const isDataValid = await this.$refs.form.validate();
      if (!isDataValid) {
        return;
      }

      this.awaitingResponse = true;

      console.log("Student:\n", this.student);
      try {
        await registerStudent(this.student);
        this.$emit("registration-completed");
      } catch (e) {
        postError("студента", e.response?.status);
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
