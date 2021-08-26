<template>
  <div :class="$style.root">
    <PrimeTabMenu :model="tabs" />

    <router-view :class="$style.page" />
  </div>
</template>

<script>
import { Component, Vue, Watch } from "vue-property-decorator";
import { hasPermission } from "@/utils/permissions";
import { UserModule } from "@/store";

@Component({
  name: "AdminPanelPage",
})
class AdminPanelPage extends Vue {
  defaultTabs = [
    { label: "Подтверждения регистрации", to: "/apanel/approve/", permissions: [] },
    { label: "Управление пользователями", to: "/apanel/userManagement/", permissions: ["permissions.get.all", "permissions.patch.all", "permissions.post.all", "permissions.delete.all"] },
    { label: "Управление ролями", to: "/apanel/roleManagement/", permissions: ["permissions.get.all", "permissions.patch.all", "permissions.post.all", "permissions.delete.all"] },
    { label: "Справочники", to: "/apanel/dictionaries/", permissions: [] },
    { label: "Учебные дисциплины", to: "/apanel/subjects/", permissions: ["subjects.get.all", "subjects.get.self", "subjects.post.all", "subjects.patch.all", "subjects.delete.all"] },
  ]

  tabs = []

  get permissions() { return UserModule.permissions; }

  mounted() {
    this.getTabs();
  }

  getTabs() {
    console.count();
    const tabs = this.defaultTabs.filter(item => hasPermission(item.permissions));
    this.tabs = tabs;

    const currentPath = this.$route.path;
    if (!tabs.find(item => item.to === currentPath)) {
      if (tabs.length) {
        this.$router.push(tabs[0].to);
      }
    }
  }

  @Watch("permissions")
  onPermissionsChange() {
    this.getTabs();
  }
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
