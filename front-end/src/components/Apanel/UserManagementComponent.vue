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
        :key="item.user_id"
        :label="item.fullname"
        :value="item.user_id"
      />
    </el-select>

    <el-row v-if="userId" class="content">
      <el-col :span="3">
        <div
          :class="[mode === 'role' ? 'active' : 'not-active', 'tab-button']"
          @click="() => selectMode('role')"
        >
          Роли
        </div>
        <div
          :class="[mode === 'role' ? 'not-active' : 'active', 'tab-button']"
          @click="() => selectMode('permissions')"
        >
          Права
        </div>
      </el-col>
      <el-col :span="20" :offset="1">
        <div v-if="mode === 'role'" v-loading="permissionLoading" class="permission-content">
          <el-transfer
            v-model="roleValue"
            filterable
            :titles="['Все роли', 'Текущие роли']"
            :data="roleData"
            @change="(data) => changeInUserControl({ groups: data })"
          />
        </div>

        <div v-if="mode === 'permissions'" v-loading="permissionLoading" class="permission-content">
          <el-transfer
            v-model="permissionValue"
            filterable
            :titles="['Все права доступа', 'Текущие права доступа']"
            :data="permissionData"
            @change="(data) => changeInUserControl({ permissions: data })"
          />
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import _throttle from "lodash/throttle";

import {
  getUsers,
  getUserPermissions,
  getAllPermissions,
  saveUserControl,
  getAllRoles,
} from "@/api/admin";
import { hasPermission } from "@/utils/permissions";

export default {
  name: "UserManagementComponent",
  data() {
    return {
      mode: "role",
      permissionData: [],
      permissionValue: [],
      roleData: [],
      roleValue: [],
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
    selectMode(mode) {
      this.mode = mode;
    },
    changeInUserControl(data) {
      if (hasPermission(["permissions.patch.all"])) {
        saveUserControl(this.userId, data).catch(err => {
          this.$message.error("Ошибка редактирования данных о пользователе");
          console.log("[UserManagementComponent Error]: ", err);
        });
      } else {
        this.$message.error("У вас нет доступа для этого действия");
      }
    },
    selectUserHandler(userId) {
      this.permissionLoading = true;
      getUserPermissions(userId)
        .then(res => {
          this.permissionLoading = false;
          this.permissionValue = res.data.permissions;
          this.roleValue = res.data.groups;
        })
        .catch(err => {
          this.$message.error("Ошибка загрузки прав пользователя");
          console.log("[UserManagementComponent Error]: ", err);
          this.permissionLoading = false;
        });
    },
    remoteMethod: _throttle(function request(name) {
      if (name) {
        this.loading = true;
        getUsers({ name })
          .then(res => {
            this.options = res.data;
          })
          .catch(err => {
            console.log("[UserManagementComponent Error]: ", err);
            this.$message.error("Ошибка загрузки данных о пользователях");
          })
          .finally(() => { this.loading = false; });
      } else {
        this.options = [];
      }
    }, 500),
    async fetchData() {
      try {
        this.roleData = (await getAllRoles()).data;
        this.permissionData = (await getAllPermissions()).data;
      } catch (err) {
        this.$message.error("Ошибка загрузки данных о правах доступа");
        console.log("[UserManagementComponent Error]: ", err);
      }
    },
  },
};
</script>

<style scoped lang="scss">
@import "@/styles/variables.scss";

.tab-button {
  width: 196px;
  height: 33px;
  font-family: 'Proxima Nova';
  border-radius: 8px;
  font-style: normal;
  font-weight: normal;
  cursor: pointer;
  display: flex;
  align-items: center;
  padding: 9px 12px;
  margin-bottom: 8px;
}

.active {
  background: #F6F7FB;
  font-weight: 600;
  font-size: 14px;
  color: #0C4B9A;
}
.not-active {
  border: 1px solid #F2F2F2;
  box-sizing: border-box;
  font-size: 14px;
  color: #858587;
}

.content {
  padding-top: $xl;
}

.el-select {
  width: 100%;
}

.el-transfer {
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
