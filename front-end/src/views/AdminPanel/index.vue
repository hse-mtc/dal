<template>
  <div class="root">
    <el-tabs v-model="activeTab" @tab-click="handleClick">
      <el-tab-pane label="Подтверждения регистрации" name="approve">
        <Approve />
      </el-tab-pane>
      <el-tab-pane label="Разрешения" name="permissions">
        <PermissionComponent />
      </el-tab-pane>
      <el-tab-pane label="Справочники" name="dictionaries">
        <!-- DictionariesComponent -->
      </el-tab-pane>
      <el-tab-pane label="Учебные дисциплины" name="subjects">
        <SubjectsControl />
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import PermissionComponent from "@/components/Apanel/PermissionComponent";
import Approve from "@/components/Apanel/Approve/Approve";
import SubjectsControl from "@/components/Apanel/SubjectsControl";

export default {
  components: { Approve, PermissionComponent, SubjectsControl },
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
