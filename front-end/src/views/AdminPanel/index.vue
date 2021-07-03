<template>
  <div :class="$style.root">
    <PrimeTabMenu :model="tabs">
      <el-tab-pane label="Подтверждения регистрации" name="approve" />
      <el-tab-pane label="Разрешения" name="permissions" />
      <el-tab-pane label="Справочники" name="dictionaries" />
      <el-tab-pane label="Учебные дисциплины" name="subjects" />
    </PrimeTabMenu>

    <router-view :class="$style.page" />
  </div>
</template>

<script>
import { Component } from "vue-property-decorator";

@Component({
  name: "AdminPanelPage",
})
class AdminPanelPage {
  tabs = [
    { label: "Подтверждения регистрации", to: "/apanel/approve/" },
    { label: "Разрешения", to: "/apanel/permissions/" },
    { label: "Справочники", to: "/apanel/dictionaries/" },
    { label: "Учебные дисциплины", to: "/apanel/subjects/" },
  ]
}

export default AdminPanelPage;
</script>

<style lang="scss" module>
.root {
  margin: 50px;
}

.page {
  margin-top: 50px;
}
</style>
