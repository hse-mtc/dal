<template>
  <div class="change-password-container">
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
  </div>
</template>

<script>
import { changePassword } from "@/api/user";
import jwtDecode from "jwt-decode";
import { UserModule } from "@/store";

export default {
  name: "ChangePassword",
  data() {
    const validatePassword = (rule, value, callback) => {
      if (value.length < 6) {
        callback(new Error("Пароль не должен содержать менее 6 символов"));
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
    let { token } = this.$route.query;
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
      console.log(1);
      this.$refs.changePasswordForm.validate(async valid => {
        console.log(2);
        if (valid) {
          this.loading = true;
          try {
            await changePassword({ password: this.changePasswordForm.password });
            UserModule.resetToken()
              .then(() => {
                this.$router.push({ path: "/login" });
                this.loading = false;
              })
              .catch(() => {
                this.loading = false;
              });
            return true;
          } catch (e) {
            this.loading = false;
            return false;
          }
        }
        console.log("error submit!");
        return false;
      });
    },
  },
};
</script>

<style lang="scss">
$bg: #283443;
$light_gray: #fff;
$cursor: #fff;
@supports (-webkit-mask: none) and (not (cater-color: $cursor)) {
  .change-password-container .el-input input {
    color: $cursor;
  }
}
/* reset element-ui css */
.change-password-container {
  .el-input {
    display: inline-block;
    height: 47px;
    width: 85%;
    input {
      background: transparent;
      border: 0px;
      -webkit-appearance: none;
      border-radius: 0px;
      padding: 12px 5px 12px 15px;
      color: $light_gray;
      height: 47px;
      caret-color: $cursor;
      &:-webkit-autofill {
        box-shadow: 0 0 0px 1000px $bg inset !important;
        -webkit-text-fill-color: $cursor !important;
      }
    }
  }
  .el-form-item {
    border: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(0, 0, 0, 0.1);
    border-radius: 5px;
    color: #454545;
  }
}
</style>

<style lang="scss" scoped>
$bg: #2d3a4b;
$dark_gray: #889aa4;
$light_gray: #eee;
.change-password-container {
  min-height: 100%;
  width: 100%;
  background-color: $bg;
  overflow: hidden;
  .change-password-form {
    position: relative;
    width: 520px;
    max-width: 100%;
    padding: 160px 35px 0;
    margin: 0 auto;
    overflow: hidden;
  }
  .tips {
    font-size: 14px;
    color: #fff;
    margin-bottom: 10px;
    span {
      &:first-of-type {
        margin-right: 16px;
      }
    }
  }
  .svg-container {
    padding: 6px 5px 6px 15px;
    color: $dark_gray;
    vertical-align: middle;
    width: 30px;
    display: inline-block;
  }
  .title-container {
    position: relative;
    .title {
      font-size: 26px;
      color: $light_gray;
      margin: 0px auto 40px auto;
      text-align: center;
      font-weight: bold;
    }
  }
  .show-pwd {
    position: absolute;
    right: 10px;
    top: 7px;
    font-size: 16px;
    color: $dark_gray;
    cursor: pointer;
    user-select: none;
  }
}
</style>
