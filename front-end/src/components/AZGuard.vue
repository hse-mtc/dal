<template>
  <span v-if="disable || hasPermission">
    <el-tooltip :disabled="!disabled || !tooltip" content="Нет доступа">
      <span>
        <slot :disabled="disabled" />
      </span>
    </el-tooltip>
  </span>
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
    disable: {
      type: Boolean,
      default: false,
    },
    tooltip: {
      type: Boolean,
      default: true,
    },
  },
  computed: {
    disabled() {
      return this.disable && !this.hasPermission;
    },
    usersPermissions() {
      return UserModule.permissions;
    },
    isSuperuser() {
      return UserModule.isSuperuser;
    },
    hasPermission() {
      if (!this.isSuperuser) {
        if (this.permissions?.length) {
          return this.permissions.some(permission => {
            if (typeof permission === "string") {
              return this.usersPermissions.find(
                userPermission => userPermission.codename === permission,
              );
            }
            if (typeof permission === "object") {
              return this.usersPermissions.find(
                userPermission => userPermission.codename === permission.codename
                  && permission.validator(),
              );
            }
            return false;
          });
        }
      }
      return true;
    },
  },
};
</script>

<style scoped></style>
