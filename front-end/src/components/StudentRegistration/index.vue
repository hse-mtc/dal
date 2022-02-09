<template>
  <ElRow
    class="register"
    type="flex"
  >
    <ElCol
      :xl="12"
      :lg="12"
      class="register-col"
    >
      <div class="register-container">
        <div class="register-form">
          <div class="title-container">
            <h2 class="title">
              Даль ВУЦ ВШЭ
            </h2>
          </div>

          <div class="title-container">
            <h3 class="sub-title">
              Регистрация
              {{ personnelToRegisterTitle }}
            </h3>
          </div>

          <!-- eslint-disable vue/html-quotes -->
          <RegisterStudent
            v-if='personnel === "student"'
            @registration-completed="registrationCompleted"
          />
          <!-- eslint-enable vue/html-quotes -->
        </div>
      </div>

      <ElDialog
        :close-on-click-modal="false"
        :close-on-press-escape="false"
        :show-close="false"
        title="Регистрация завершена"
        :visible.sync="registrationComplete"
      >
        <p>
          Ожидайте подтверждения регистрации.
        </p>
        <p>
          После подтверждения на Вашу почту будет выслана ссылка для создания пароля.
        </p>
      </ElDialog>
    </ElCol>
    <ElCol
      :span="12"
      class="hidden-md-and-down register-col register-col-last"
    />
  </ElRow>
</template>

<script>
import RegisterStudent from "@/components/StudentRegistration/Student";

export default {
  components: { RegisterStudent },

  data() {
    return {
      personnel: "student",
      registrationComplete: false,
    };
  },

  computed: {
    personnelToRegisterTitle() {
      switch (this.personnel) {
        case "student":
          return "студента";
        default:
          return "";
      }
    },
  },

  methods: {
    registrationCompleted() {
      this.registrationComplete = true;
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
