<template>
  <div class="root">
    <el-tabs v-model="activeTab" @tab-click="handleClick">
      <el-tab-pane label="Подтверждения регистрации" name="approve">
        <!-- ApproveComponent -->
      </el-tab-pane>
      <el-tab-pane label="Разрешения" name="permissions">
        <PermissionComponent />
      </el-tab-pane>
      <el-tab-pane label="Справочники" name="dictionaries">
        <!-- DictionariesComponent -->
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import PermissionComponent from "@/components/Apanel/PermissionComponent";

export default {
  components: { PermissionComponent },
  data() {
    return {
      activeTab: "approve",
    };
  },
  methods: {
    handleClick() {},
  },
};
</script>

<style scoped lang="scss">
@import "@/styles/variables.scss";

.root {
  padding: $xl;
}
</style>
