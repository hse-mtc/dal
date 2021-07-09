<template>
  <div class="permission-root">
    <el-select
      v-model="roleId"
      filterable
      clearable
      reserve-keyword
      placeholder="Введите название роли"
      :loading="loading"
      @change="selectRoleHandler"
    >
      <el-option
        v-for="item in options"
        :key="item.key"
        :label="item.label"
        :value="item.key"
      />
    </el-select>

    <el-row class="pageTitle">
      <el-col :span="24">
        <div class="d-flex align-items-center justify-content-end">
          <CustomText
            v-if="roleId"
            variant="paragraph"
            :custom-style="{ color: '#409EFF', cursor: 'pointer', marginRight: '16px' }"
          >
            <div @click="deleteRoleHandler">
              Удалить текущую роль
            </div>
          </CustomText>

          <CustomText
            variant="paragraph"
            :custom-style="{ color: '#409EFF', cursor: 'pointer' }"
          >
            <div @click="windowModal = true">
              + Добавить новую роль
            </div>
          </CustomText>
        </div>
      </el-col>
    </el-row>

    <div v-if="roleId" v-loading="permissionLoading" class="permission-content">
      <el-transfer
        v-model="permissionValue"
        filterable
        :titles="['Все права доступа', 'Права доступа принадлежащие роли']"
        :data="permissionData"
        @change="(data) => changeInRole({ permissions: data })"
      />
    </div>

    <ModalWindow :opened="windowModal" @closeModal="closeModal">
      <CustomText :mb="SIZES.m" :custom-style="{ 'font-weight': 'normal' }" variant="header">
        Добавление роли
      </CustomText>
      <ElForm
        ref="roleForm"
        class="role-form"
        :rules="rules"
        :model="roleForm"
        label-width="180px"
      >
        <ElFormItem label="Название роли" prop="title">
          <ElInput v-model="roleForm.name" placeholder="Введите название" />
        </ElFormItem>

        <ElFormItem>
          <ElButton type="primary" @click="submitForm">
            Отправить
          </ElButton>
          <ElButton @click="closeModal">
            Отменить
          </ElButton>
        </ElFormItem>
      </ElForm>
    </ModalWindow>
  </div>
</template>

<script>
import {
  deleteRole,
  getRolePermissions,
  saveRoleChanges,
  getAllRoles,
  getAllPermissions,
  addRole,
} from "@/api/admin";
import CustomText from "@/common/CustomText";
import ModalWindow from "@/components/ModalWindow/ModalWindow.vue";
import { SIZES } from "@/utils/appConsts";
import { Message } from "element-ui";

export default {
  name: "RoleManagementComponent",
  components: { CustomText, ModalWindow },
  data() {
    return {
      SIZES,
      windowModal: false,
      roleForm: {
        name: "",
        permissions: [],
      },
      rules: {
        name: [{ required: true, message: "Обязательное поле" }],
      },
      permissionData: [],
      permissionValue: [],
      options: [],
      roleId: null,
      loading: false,
      permissionLoading: false,
    };
  },
  created() {
    this.fetchData();
  },
  methods: {
    async deleteRoleHandler() {
      await this.$confirm(
        "Вы уверены, что хотите удалить роль?",
        "Подтверждение",
        {
          confirmButtonText: "Да",
          cancelButtonText: "Отмена",
          type: "warning",
        },
      );
      try {
        await deleteRole(this.roleId);
        this.options = this.options.filter(i => i.key !== this.roleId);
        this.roleId = null;
      } catch (e) {
        Message({
          message: "Не получилось удалить роль",
          type: "error",
        });
      }
    },
    submitForm() {
      this.$refs.roleForm.validate(async valid => {
        if (valid) {
          if (await addRole(this.roleForm)) {
            this.loading = true;
            this.options = (await getAllRoles()).data;
            this.loading = false;
            this.closeModal();
          } else {
            Message({
              message: "Ошибка отправки формы",
              type: "error",
            });
          }
        }
      });
    },
    closeModal() {
      this.subjectForm = {
        title: "",
      };
      this.windowModal = false;
    },
    changeInRole(data) {
      saveRoleChanges(this.roleId, data).catch(err => {
        this.$message.error("Ошибка редактирования данных о роли");
        console.log("[RoleManagementComponent Error]: ", err);
      });
    },
    selectRoleHandler(roleId) {
      this.permissionLoading = true;
      getRolePermissions(roleId)
        .then(res => {
          this.permissionLoading = false;
          this.permissionValue = res.data.permissions;
        })
        .catch(err => {
          this.$message.error("Ошибка загрузки прав доступа для роли");
          console.log("[RoleManagementComponent Error]: ", err);
          this.permissionLoading = false;
        });
    },
    async fetchData() {
      try {
        this.loading = true;
        this.options = (await getAllRoles()).data;
        this.permissionData = (await getAllPermissions()).data;
        this.loading = false;
      } catch (err) {
        this.$message.error("Ошибка загрузки данных о ролях");
        console.log("[RoleManagementComponent Error]: ", err);
      }
    },
  },
};
</script>

<style scoped lang="scss">
@import "@/styles/variables.scss";

.pageTitle {
  margin-top: 8px;
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