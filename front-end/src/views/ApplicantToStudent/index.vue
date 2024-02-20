<template>
  <div class="app-container">
    <Register v-if="userId !== null" :user-id="userId" />
  </div>
</template>

<script>
import Register from "@/components/ApplicantToStudent/index";
import { UserModule } from "@/store";

export default {
  components: { Register },
  data() {
    return {
      userId: null,
    };
  },
  mounted() {
    const { userId } = this.$route.query;
    if (userId === undefined) {
      this.userId = UserModule.personId;
    } else {
      this.userId = userId;
    }
  },
};
</script>
