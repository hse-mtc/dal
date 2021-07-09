<template>
  <div v-if="hasPermission">
    <slot />
  </div>
</template>

<script>
import { UserModule } from "@/store";

export default {
  name: "AZGuard",
  props: {
    permissions: {
      type: Array,
      default: () => [],
    },
  },
  computed: {
    usersPermissions() { return UserModule.permissions; },
    hasPermission() {
      if (this.permissions?.length) {
        // eslint-disable-next-line max-len
        return this.permissions.some(permission => (this.usersPermissions.find(userPermission => userPermission.codename === permission)));
      }
      return true;
    },
  },
};
</script>

<style scoped>

</style>
