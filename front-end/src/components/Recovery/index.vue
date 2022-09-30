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

    <el-form-item prop="email">
      <el-input
        ref="email"
        v-model="recoveryForm.email"
        placeholder="mail@example.com"
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
</style>
