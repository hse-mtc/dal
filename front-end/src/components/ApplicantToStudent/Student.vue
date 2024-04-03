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
        Взвод
      </div>
      <ElFormItem prop="milgroup">
        <ElSelect v-model="student.milgroup" placeholder="Выберите свой взвод" style="display: block">
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
        <ElSelect v-model="student.post" placeholder="Выберите должность" style="display: block">
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
import { registerStudentFromApplicant } from "@/api/user";
import { findApplicant } from "@/api/applicants";

export default {
  mixins: [StudentPostsMixin],

  props: {
    userId: {
      type: [String, Number],
      required: true,
    },
  },

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
      trigger: "blur",
      validator: validateEmail,
    };

    return {
      awaitingResponse: false,

      student: {
        milgroup: null,
        post: null,
        university_info: null,
      },

      rules: {
        milgroup: [requiredRule],
        rank: [requiredRule],
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

    this.studentPosts.PRIVATE_STUDENT = { label: "-", value: null };

    const response = await findApplicant(this.userId);

    const { data } = response;
    delete data.family;
    delete data.photo;

    const programId = data.university_info.program.id;

    this.student = { ...this.student, ...data };
    this.student.university_info.program = programId;
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
        await registerStudentFromApplicant(this.student);
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
