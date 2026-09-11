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
            <AZGuard :permissions="['applicants.get.all']">
              <a
                :href="getApplicantAdminUrl(userId)"
                target="_blank"
                rel="noopener noreferrer"
                class="django-admin-link"
              >
                <ElButton size="small" icon="el-icon-setting">
                  Открыть в Django Admin
                </ElButton>
              </a>
            </AZGuard>
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
import { getApplicantAdminUrl } from "@/utils/djangoAdmin";

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

  methods: {
    getApplicantAdminUrl,
    registrationCompleted() {
      this.registrationComplete = true;
      setTimeout(() => {
        this.$router.replace({ name: "Login" });
      }, 7000);
    },
  },
};
</script>

<style lang="scss" scoped>
@import "style";

.django-admin-link {
  display: inline-block;
  margin-top: 12px;
}
</style>
