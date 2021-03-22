<template>
  <div>
    <el-tabs v-model="activeTab" @tab-click="handleClick">
      <el-tab-pane label="Подтверждения регистрации" name="approve">
        <!-- ApproveComponent -->
      </el-tab-pane>
      <el-tab-pane label="Разрешения" name="permissions">
        <!-- PermissionsComponent -->
      </el-tab-pane>
      <el-tab-pane label="Справочники" name="dictionaries">
        <!-- DictionariesComponent -->
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
export default {
  components: {},
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
