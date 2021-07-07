<template>
  <el-form
    ref="changePasswordForm"
    :model="changePasswordForm"
    :rules="changePasswordRules"
    class="change-password-form"
    label-position="left"
  >
    <div class="title-container">
      <h3 class="title">
        Смена пароля
      </h3>
    </div>

    <el-form-item prop="password">
      <el-input
        ref="password"
        v-model="changePasswordForm.password"
        placeholder="Новый пароль"
        name="password"
        :type="passwordType"
        tabindex="1"
      />
      <span class="show-pwd" @click="showPwd">
        <svg-icon
          :icon-class="passwordType === 'password' ? 'eye' : 'eye-open'"
        />
      </span>
    </el-form-item>

    <el-form-item prop="passwordAgain">
      <el-input
        :key="passwordType"
        ref="passwordAgain"
        v-model="changePasswordForm.passwordAgain"
        :type="passwordType"
        placeholder="Повторите пароль"
        name="passwordAgain"
        tabindex="2"
      />
    </el-form-item>

    <el-button
      :loading="loading"
      type="primary"
      style="width: 100%; margin-bottom: 30px"
      @click="handleChangePassword"
    >
      Подтвердить
    </el-button>
  </el-form>
</template>

<script>
import { changePassword } from "@/api/user";
import jwtDecode from "jwt-decode";
import { UserModule } from "@/store";
import { patchError } from "@/utils/message";

export default {
  name: "ChangePasswordForm",
  props: {
    inDialog: Boolean,
  },
  data() {
    const validatePassword = (rule, value, callback) => {
      if (value.length < 6) {
        callback(new Error("Пароль должен содержать не менее 6 символов"));
      } else {
        callback();
      }
    };
    const validatePasswordAgain = (rule, value, callback) => {
      if (value !== this.changePasswordForm.password) {
        callback(new Error("Пароли не совпадают"));
      } else {
        callback();
      }
    };
    return {
      changePasswordForm: {
        password: "",
        passwordAgain: "",
      },
      changePasswordRules: {
        password: [
          { required: true, trigger: "blur", validator: validatePassword },
        ],
        passwordAgain: [
          { required: true, trigger: "blur", validator: validatePasswordAgain },
        ],
      },
      loading: false,
      passwordType: "password",
    };
  },
  created() {
    if (!this.inDialog) {
      let { token } = this.$route.query;
      console.log("🚀 > token", token);
      try {
        jwtDecode(token);
      } catch (ex) {
        token = null;
      }
      if (!token) {
        this.$router.push({ path: "/" });
        return;
      }
      UserModule.setToken(token);
    }
  },
  methods: {
    showPwd() {
      if (this.passwordType === "password") {
        this.passwordType = "";
      } else {
        this.passwordType = "password";
      }
      this.$nextTick(() => {
        this.$refs.password.focus();
      });
    },
    handleChangePassword() {
      this.$refs.changePasswordForm.validate(async valid => {
        if (valid) {
          this.loading = true;
          try {
            await changePassword({
              password: this.changePasswordForm.password,
            });
            if (!this.inDialog) {
              UserModule.resetToken()
                .then(() => {
                  this.$router.push({ path: "/login" });
                });
            }
            this.$emit("submited");
            return true;
          } catch (err) {
            patchError("пароля", err.response.status);
            return false;
          } finally {
            this.loading = false;
          }
        }
        return false;
      });
    },
  },
};
</script>

<style lang="scss" scoped>
@import "style";
</style>
