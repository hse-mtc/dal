<template>
  <el-form
    ref="recoveryForm"
    :model="recoveryForm"
    :rules="recoveryRules"
    class="recovery-form"
    label-position="left"
  >
    <div class="title-container">
      <h3 class="title">
        Восстановление пароля
      </h3>
    </div>

    <p class="email-hint">
      Для студентов и преподавателей используйте корпоративную почту ВШЭ
      (`@hse.ru` или `@edu.hse.ru`). Абитуриентам нужно указать адрес,
      использованный при регистрации.
    </p>

    <el-form-item prop="email">
      <el-input
        ref="email"
        v-model.trim="recoveryForm.email"
        placeholder="Введите email"
        name="email"
        type="text"
        tabindex="1"
        auto-complete="on"
      />
    </el-form-item>

    <el-button
      :loading="loading"
      type="primary"
      style="width: 100%; margin-bottom: 30px"
      @click="emailPassed"
    >
      Продолжить
    </el-button>
  </el-form>
</template>

<script>
import { validEmail } from "@/utils/validate";
import { Message } from "element-ui";
import { sendRecoveryEmail } from "@/api/recovery";

export default {
  name: "RecoveryForm",
  data() {
    const validateEmail = (rule, value, callback) => {
      if (!validEmail(value)) {
        callback(new Error("Пожалуйста, введите корректную почту"));
      } else {
        callback();
      }
    };
    return {
      recoveryForm: {
        email: "",
      },
      recoveryRules: {
        email: [{ required: true, trigger: "blur", validator: validateEmail }],
      },
      loading: false,
    };
  },
  methods: {
    async emailPassed() {
      await sendRecoveryEmail(this.recoveryForm);
      Message({
        message: "На указанную почту была выслана ссылка для задания пароля",
        type: "success",
      });
      setTimeout(() => {
        this.$router.replace({ name: "Login" });
      }, 4000);
    },
  },
};
</script>

<style lang="scss" scoped>
    @import "style";

    .email-hint {
      font-size: 14px;
      line-height: 1.45;
      color: #889aa4;
      margin: -24px 0 20px;
      text-align: center;
    }
</style>
