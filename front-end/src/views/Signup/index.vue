<template>
  <el-row class="register" type="flex">
    <el-col :xl="12" :lg="12" class="register-col">
      <div v-if="!finished" class="register-container">
        <el-form
          ref="registerForm"
          :model="registerForm"
          :rules="loginRules"
          class="register-form"
          auto-complete="on"
          label-position="left"
        >
          <div class="title-container">
            <h2 class="title">
              Даль ВУЦ
            </h2>
          </div>

          <div class="title-container">
            <h3 class="sub-title">
              Регистрация
            </h3>
          </div>
          <div class="field-title">
            Корпоративная почта ВШЭ
          </div>
          <el-form-item prop="email">
            <el-input
              ref="email"
              v-model="registerForm.email"
              placeholder="Укажите email"
              name="email"
              type="text"
              tabindex="1"
              auto-complete="on"
            />
          </el-form-item>

          <div>
            <div style="width: 45%">
              <div class="field-title">
                Роль
              </div>
              <el-form-item prop="role">
                <el-select
                  v-model="registerForm.role"
                  placeholder="Выберите роль"
                  style="display: block"
                >
                  <el-option
                    v-for="item in roles"
                    :key="item.key"
                    :label="item.label"
                    :value="item.key"
                  />
                </el-select>
              </el-form-item>
            </div>
            <div v-if="registerForm.role === 'student'" style="width: 45%">
              <div class="field-title">
                Взвод
              </div>
              <el-form-item prop="milgroup">
                <el-select
                  v-model="registerForm.milgroup"
                  placeholder="Выберите взвод"
                  style="display: block"
                >
                  <el-option
                    v-for="milgroup in milgroups"
                    :key="milgroup.id"
                    :label="milgroup.title"
                    :value="milgroup.id"
                  />
                </el-select>
              </el-form-item>
            </div>

            <template v-if="registerForm.role === 'teacher'">
              <div class="field-title">
                Фамилия
              </div>
              <el-form-item prop="lastName">
                <el-input
                  ref="lastName"
                  v-model="registerForm.lastName"
                  placeholder="Укажите фамилия"
                  name="lastName"
                  type="text"
                  tabindex="1"
                  auto-complete="on"
                />
              </el-form-item>

              <div class="" style="display: flex">
                <div style="width: 45%">
                  <div class="field-title">
                    Имя
                  </div>
                  <el-form-item prop="firstName">
                    <el-input
                      ref="firstName"
                      v-model="registerForm.firstName"
                      placeholder="Укажите имя"
                      name="firstName"
                      type="text"
                      tabindex="1"
                      auto-complete="on"
                    />
                  </el-form-item>
                </div>

                <div style="margin-left: 63px; width: 45%">
                  <div class="field-title">
                    Отчество
                  </div>
                  <el-form-item prop="patronymic">
                    <el-input
                      ref="patronymic"
                      v-model="registerForm.patronymic"
                      placeholder="Укажите отчество"
                      name="patronymic"
                      type="text"
                      tabindex="1"
                      auto-complete="on"
                    />
                  </el-form-item>
                </div>
              </div>

              <div class="field-title">
                Цикл
              </div>
              <el-form-item prop="role">
                <el-select
                  v-model="registerForm.milfaculty"
                  placeholder="Выберите цикл"
                  style="display: block"
                >
                  <el-option
                    v-for="milfaculty in milfaculties"
                    :key="milfaculty.id"
                    :label="milfaculty.title"
                    :value="milfaculty.id"
                  />
                </el-select>
              </el-form-item>

              <div class="field-title">
                Звание
              </div>
              <el-form-item prop="role">
                <el-select
                  v-model="registerForm.rank"
                  placeholder="Выберите звание"
                  style="display: block"
                >
                  <el-option
                    v-for="rank in teacherRanks"
                    :key="rank.value"
                    :label="rank.label"
                    :value="rank.value"
                  />
                </el-select>
              </el-form-item>

              <div class="field-title">
                Должность
              </div>
              <el-form-item prop="role">
                <el-select
                  v-model="registerForm.post"
                  placeholder="Выберите должность"
                  style="display: block"
                >
                  <el-option
                    v-for="post in teacherPosts"
                    :key="post.value"
                    :label="post.label"
                    :value="post.value"
                  />
                </el-select>
              </el-form-item>

              <div class="field-title">
                Прикрепленный взвод
              </div>
              <el-form-item prop="milgroup">
                <el-select
                  v-model="registerForm.supervisedMilgroup"
                  placeholder="Выберите взвод"
                  style="display: block"
                >
                  <el-option
                    v-for="milgroup in milgroups"
                    :key="milgroup.id"
                    :label="milgroup.title"
                    :value="milgroup.id"
                  />
                </el-select>
              </el-form-item>
            </template>
          </div>

          <el-button
            :loading="loading"
            type="primary"
            :disabled="disabledButton"
            style="width: 190px; margin-bottom: 30px; margin-top: 20px"
            @click.native.prevent="handleRegister"
          >
            Зарегистрироваться
          </el-button>
        </el-form>
        <div class="register">
          Уже есть аккаунт?
          <router-link
            style="color: #007bff"
            :to="{ name: 'Login' }"
            replace
          >
            Войти
          </router-link>
        </div>
      </div>
      <el-dialog
        :close-on-click-modal="false"
        :close-on-press-escape="false"
        :show-close="false"
        title="Спасибо за регистрацию"
        :visible.sync="finished"
      >
        <div>
          Ожидайте подтверждения регистрации.
          После подтверждения на почту будет выслана ссылка для создания пароля.
        </div>
      </el-dialog>
    </el-col>
    <el-col
      :span="12"
      class="hidden-md-and-down register-col register-col-last"
    />
  </el-row>
</template>

<script>
import { validCorEmail } from "@/utils/validate";
import {
  getMilFaculties,
  getMilGroups,
} from "@/api/reference-book";
import { registerStudent, registerTeacher } from "@/api/user";
import { teacherPostMixin, teacherRankMixin } from "@/mixins/teachers";

export default {
  name: "Signup",
  mixins: [teacherPostMixin, teacherRankMixin],

  data() {
    const validateEmail = (rule, value, callback) => {
      if (!validCorEmail(value)) {
        callback(new Error("Пожалуйста, введите корректный email"));
      } else {
        callback();
      }
    };

    return {
      registerForm: {
        email: "",
        role: "",
        firstName: "",
        lastName: "",
        patronymic: "",
        milgroup: "",
        supervisedMilgroup: "",
        post: "",
        milfaculty: "",
        rank: "",
      },
      milgroups: [],
      milfaculties: [],
      roles: [
        { label: "Студент", key: "student" },
        { label: "Преподаватель", key: "teacher" },
      ],
      finished: false,
      loginRules: {
        email: [{ required: true, trigger: "blur", validator: validateEmail }],
      },
      loading: false,
      passwordType: "password",
      redirect: undefined,
    };
  },

  computed: {
    disabledButton() {
      if (this.registerForm.role === "student") {
        return (
          !this.registerForm.role
          || !this.registerForm.milgroup
          || !this.registerForm.email
        );
      }
      if (this.registerForm.role === "teacher") {
        return (
          !this.registerForm.firstName
          || !this.registerForm.lastName
          || !this.registerForm.patronymic
          || !this.registerForm.supervisedMilgroup
          || !this.registerForm.post
          || !this.registerForm.milfaculty
          || !this.registerForm.rank
        );
      }
      return true;
    },
  },

  watch: {
    $route: {
      handler(route) {
        this.redirect = route.query && route.query.redirect;
      },
      immediate: true,
    },
  },

  async created() {
    await this.fetchData();
  },

  methods: {
    async fetchData() {
      const responses = await Promise.all([
        getMilGroups(),
        getMilFaculties(),
      ]);
      [this.milgroups, this.milfaculties] = responses.map(r => r.data);
    },

    handleRegister() {
      this.$refs.registerForm.validate(valid => {
        if (valid) {
          this.loading = true;
          if (this.registerForm.role === "student") {
            const data = {
              email: this.registerForm.email,
              milgroup: this.registerForm.milgroup,
            };
            registerStudent(data)
              .then(response => {
                this.loading = false;
                this.finished = true;
                setTimeout(() => {
                  this.$router.replace({ path: "login" });
                }, 4000);
              })
              .catch(() => {
                this.loading = false;
                this.$message({
                  type: "error",
                  message: "Ошибка регистрации",
                });
              });
          }
          if (this.registerForm.role === "teacher") {
            const data = {
              firstName: this.registerForm.firstName,
              lastName: this.registerForm.lastName,
              patronymic: this.registerForm.patronymic,
              supervisedMilgroup: this.registerForm.supervisedMilgroup,
              post: this.registerForm.post,
              milfaculty: this.registerForm.milfaculty,
              rank: this.registerForm.rank,
            };
            registerTeacher(data)
              .then(response => {
                this.loading = false;
                this.finished = true;
                setTimeout(() => {
                  this.$router.replace({ path: "login" });
                }, 4000);
              })
              .catch(() => {
                this.loading = false;
                this.$message({
                  type: "error",
                  message: "Ошибка регистрации",
                });
              });
          }
        }
      });
    },
  },
};
</script>

<style lang="scss" scoped>
$cursor: #fff;
$bg: #fff;
$dark_gray: #889aa4;
$light_gray: #eee;
.finished {
  margin-top: 100px;
  text-align: center;
}
.autocomplete-fields {
  margin-bottom: 22px;
}
.inline-input {
  border: 1px solid #e5e5e5;
  background: white;
  border-radius: 5px;
  color: #454545;
}
.register {
  color: #212529;
  text-align: center;
  margin-bottom: 40px;
}
.field-title {
  text-align: start;
  margin-bottom: 10px;
}
.register-container {
  display: flex;
  justify-content: space-between;
  flex-direction: column;
  min-height: 100%;
  width: 100%;
  background-color: $bg;
  overflow: hidden;
  .el-form-item {
    background: white;
    border-radius: 5px;
    color: #454545;
  }
  .register-form {
    position: relative;
    width: 700px;
    max-width: 100%;
    // padding: 160px 35px 0;
    padding: 50px 35px 0;
    margin: 0 auto;
    overflow: hidden;
    display: flex;
    justify-content: space-between;
    flex-direction: column;
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
    .sub-title {
      font-size: 23px;
      // color: $light_gray;
      margin: 0px auto 40px auto;
      text-align: left;
      font-weight: 600;
    }
    .title {
      font-size: 30px;
      // color: $light_gray;
      margin: 0px auto 40px auto;
      text-align: left;
      font-weight: 600;
    }
  }
  .show-pwd {
    position: absolute;
    right: 10px;
    top: 7px;
    font-size: 14px;
    color: $dark_gray;
    cursor: pointer;
    user-select: none;
  }
}
@supports (-webkit-mask: none) and (not (cater-color: $cursor)) {
  .register-container .el-input input {
    // color: $cursor;
  }
}
.register {
  min-height: 100%;
}
.register-col-last {
  background: #283443;
}
/* reset element-ui css */
.register-container {
  .el-input,
  .el-select {
    display: inline-block;
    width: 100%;
    input {
      background: transparent;
      border: 0px;
      -webkit-appearance: none;
      border-radius: 0px;
      padding: 12px 5px 12px 15px;
      color: #212529;
      height: 47px;
      // caret-color: $cursor;
      &:-webkit-autofill {
        box-shadow: 0 0 0px 1000px $bg inset !important;
        // -webkit-text-fill-color: $cursor !important;
        -webkit-text-fill-color: #606266 !important;
      }
    }
  }
}
</style>
