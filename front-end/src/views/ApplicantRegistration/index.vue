<template>
  <div class="login-container">
    <el-form
      ref="loginForm"
      :model="loginForm"
      :rules="loginRules"
      class="login-form"
      auto-complete="on"
      label-position="left"
    >
      <div class="title-container">
        <h3 class="title">
          Регистрация абитуриента
        </h3>
      </div>

      <el-form-item prop="email">
        <span class="svg-container">
          <svg-icon icon-class="user" />
        </span>
        <el-input
          ref="email"
          v-model="loginForm.email"
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
        :disabled="disablebtn"
        @click.native.prevent="handleLogin"
      >
        Зарегистрироваться
      </el-button>
    </el-form>
  </div>
</template>

<script>
import { validEmail } from "@/utils/validate";
import { UserModule } from "@/store";
import { postEmail } from "@/api/applicants";

export default {
  name: "Login",
  data() {
    const validateEmail = (rule, value, callback) => {
      if (!validEmail(value)) {
        callback(new Error("Пожалуйста, введите корректную почту"));
      } else {
        callback();
      }
    };
    return {
      disablebtn: false,
      loginForm: {
        email: "",
      },
      check: false,
      loginRules: {
        email: [{ required: true, trigger: "blur", validator: validateEmail }],
      },
      loading: false,
      redirect: undefined,
    };
  },
  watch: {
    $route: {
      handler(route) {
        this.redirect = route.query && route.query.redirect;
      },
      immediate: true,
    },
  },
  methods: {
    handleLogin() {
      this.$refs.loginForm.validate(async valid => {
        if (valid) {
          this.loading = true;
          this.disablebtn = true;
          try {
            await postEmail({
              email: this.loginForm.email,
            });
            this.$message({
              title: "Письмо отправлено",
              message: "Проверьте почту и перейдите по ссылке для задания пароля",
              type: "success",
            });
          } catch (error) {
            this.$message({
              title: "Ошибка",
              message: "Пожалуйста, введите корректную корпоративную почту",
              type: "error",
            });
          }
          this.loading = false;
          this.$router.push({ path: "/login" });
        }
      });
    },
  },
};

</script>

<style lang="scss" scoped>
$light_gray: #fff;
$cursor: #fff;
$bg: #2d3a4b;
$dark_gray: #889aa4;

@supports (-webkit-mask: none) and (not (cater-color: $cursor)) {
  .login-container .el-input input {
    color: $cursor;
  }
}


/* reset element-ui css */
.login-container {
  .el-input {
    display: inline-block;
    height: 47px;
    width: 85%;

    input {
      background: transparent !important;
      border: 0px;
      -webkit-appearance: none;
      border-radius: 0px;
      padding: 12px 5px 12px 15px;
      color: $light_gray;
      height: 47px;
      caret-color: $cursor;

      &:-webkit-autofill {
        box-shadow: 0 0 0px 1000px $bg inset !important;
        -webkit-text-fill-color: #293543 !important;
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

.login-container {
  min-height: 100%;
  width: 100%;
  background-color: $bg;
  overflow: hidden;

  .login-form {
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

.register {
  color: $light_gray;
  text-align: center;
  margin-bottom: 40px;
}
::v-deep .el-input__inner {
  color: white;
  border: none;
  background-color: transparent !important;
}
::v-deep .el-input {
  input:-webkit-autofill,
  input:-webkit-autofill:hover,
  input:-webkit-autofill:focus,
  input:-webkit-autofill:active {
    -webkit-box-shadow: 0 0 0 30px #293543 inset !important;
    -webkit-text-fill-color: white !important;
  }
}
</style>
