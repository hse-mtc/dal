<template>
  <div class="permission-root">
    <el-select
      v-model="userId"
      filterable
      clearable
      remote
      reserve-keyword
      placeholder="Введите имя пользователя"
      :remote-method="remoteMethod"
      :loading="loading"
      @change="selectUserHandler"
    >
      <el-option
        v-for="item in options"
        :key="item.id"
        :label="item.label"
        :value="item.id"
      >
      </el-option>
    </el-select>

    <div v-if="userId" class="permission-content" v-loading="permissionLoading">
      <el-transfer
        v-model="permissionValue"
        :titles="['Все роли', 'Текущие роли']"
        :data="permissionData"
        @change="changeInPermission"
      >
      </el-transfer>
    </div>
  </div>
</template>

<script>
import {
  getUsers,
  getUserPermissions,
  getAllPermissions,
  saveUserPermissions,
} from "@/api/admin";

export default {
  name: "PermissionComponent",
  data() {
    return {
      permissionData: [],
      permissionValue: [],
      options: [],
      userId: [],
      loading: false,
      permissionLoading: false,
    };
  },
  created() {
    this.fetchData();
  },
  methods: {
    changeInPermission(roles) {
      console.log(roles);
      saveUserPermissions(this.userId, roles).catch((err) => {
        this.$message.error("Ошибка редактирования прав пользователя");
        console.log("[PermissionComponent Error]: ", err);
      });
    },
    selectUserHandler(userId) {
      this.permissionLoading = true;
      getUserPermissions({ id: userId })
        .then((res) => {
          this.permissionLoading = false;
          this.permissionValue = res.data;
        })
        .catch((err) => {
          this.$message.error("Ошибка загрузки прав пользователя");
          console.log("[PermissionComponent Error]: ", err);
          this.permissionLoading = false;
          this.permissionValue = [1];
        });
    },
    remoteMethod(query) {
      if (query.length > 3) {
        this.loading = true;
        getUsers({ query })
          .then((res) => {
            this.loading = false;
            this.options = res.data;
          })
          .catch((err) => {
            this.loading = false;
            console.log("[PermissionComponent Error]: ", err);
            this.$message.error("Ошибка загрузки данных о пользователях");
            this.options = [
              {
                // Delete when BE is done
                label: "Лоскутов Владимир Михайлович",
                email: "vmloskutov@edu.hse.ru",
                id: 1,
              },
            ];
          });
      } else {
        this.options = [];
      }
    },
    fetchData() {
      getAllPermissions()
        .then((res) => {
          this.permissionData = res.data;
        })
        .catch((err) => {
          this.$message.error("Ошибка загрузки всех возможных прав доступа");
          console.log("[PermissionComponent Error]: ", err);
          this.permissionData = [
            // Delete when BE is done
            {
              label: "Роль 1",
              key: 1,
              value: 1,
            },
            {
              label: "Роль 2",
              key: 2,
              value: 2,
            },
          ];
        });
    },
  },
};
</script>

<style scoped lang="scss">
@import "@/styles/variables.scss";

.permission-root {
}

.el-select {
  width: 100%;
}

.permission-content {
  padding: $xl;
}

.el-transfer {
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
