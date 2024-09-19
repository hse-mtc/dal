<template>
  <ElRow
    class="register"
    type="flex"
  >
    <ElCol
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
              Регистрация студента ВУЦ из абитуриента
            </h3>
          </div>

          <!-- eslint-disable vue/html-quotes -->
          <Student
            :user-id="userId"
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
          Абитуриент успешно зарегистрирован в качестве студента Военного учебного центра.
        </p>
        <p>
          Информацию о нём можно просмотреть в разделе "Личный состав ВУЦ".
        </p>
      </ElDialog>
    </ElCol>
  </ElRow>
</template>

<script>
import Student from "@/components/ApplicantToStudent/Student";

export default {
  components: { Student },

  props: {
    userId: {
      type: [Number],
      required: true,
    },
  },

  data() {
    return {
      registrationComplete: false,
    };
  },

  computed: {
  },

  methods: {
    registrationCompleted() {
      this.registrationComplete = true;
      setTimeout(() => {
        this.$router.replace({ name: "Login" });
      }, 3000);
    },
  },
};
</script>

<style lang="scss" scoped>
@import "style";
</style>
