<template>
  <div :class="$style.root">
    <PrimeTabMenu :model="tabs" :active-index="null" />
    <router-view :class="$style.page" />
  </div>
</template>

<script>
import { Component, Vue } from "vue-property-decorator";
import { hasPermission } from "@/utils/permissions";
import { UserModule } from "@/store";

@Component({
  name: "AdminPanelPage",
})
class AdminPanelPage extends Vue {
  defaultTabs = [
    {
      label: "Подтверждения преподавателей", name: "Подтверждения преподавателей", to: "/apanel/approve-teachers/", permissions: ["approve-teacher.get.milfaculty"],
    },
    {
      label: "Подтверждения студентов", name: "Подтверждения студентов", to: "/apanel/approve-students/", permissions: ["approve-student.get.self"],
    },
    {
      label: "Управление пользователями", name: "Управление пользователями", to: "/apanel/userManagement/", permissions: ["permissions.patch.all"],
    },
    {
      label: "Управление ролями", name: "Управление ролями", to: "/apanel/roleManagement/", permissions: ["permissions.patch.all"],
    },
    {
      label: "Справочники", name: "Справочники", to: "/apanel/dictionaries/", permissions: ["publishers.patch.all", "authors.patch.all", "categories.patch.all", "milgroups.patch.all", "achievements.patch.all"],
    },
    {
      label: "Учебные дисциплины", name: "Учебные дисциплины", to: "/apanel/subjects/", permissions: ["approve-teacher.get.milfaculty"],
    },
  ]

  tabs = []

  get permissions() { return UserModule.permissions; }

  mounted() {
    this.getTabs();
  }

  getTabs() {
    const tabs = this.defaultTabs.filter(item => hasPermission(item.permissions));
    this.tabs = tabs;

    const currentPath = this.$route.path;
    if (!tabs.find(item => item.to === currentPath)) {
      if (tabs.length) {
        this.$router.push(tabs[0].to);
      }
    }
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
