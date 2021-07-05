<template>
  <div :class="{ 'has-logo': showLogo }">
    <Logo v-if="showLogo" :collapse="isCollapse" />

    <el-scrollbar wrap-class="scrollbar-wrapper">
      <el-menu
        :default-active="activeMenu"
        :collapse="isCollapse"
        :background-color="variables.menuBg"
        :text-color="variables.menuText"
        :unique-opened="false"
        :active-text-color="variables.menuActiveText"
        :collapse-transition="false"
        mode="vertical"
      >
        <SidebarItem
          v-for="route in routes"
          :key="route.path"
          :item="route"
          :base-path="route.path"
        />
      </el-menu>
    </el-scrollbar>
  </div>
</template>

<script>
import variables from "@/styles/variables.scss";
import { AppModule, SettingsModule } from "@/store";
import Logo from "./Logo.vue";
import SidebarItem from "./SidebarItem.vue";

export default {
  components: { SidebarItem, Logo },
  computed: {
    sidebar() { return AppModule.sidebar; },
    routes() {
      return this.$router.options.routes;
    },
    activeMenu() {
      const route = this.$route;
      const { meta, path } = route;
      // if set path, the sidebar will highlight the path you set
      if (meta.activeMenu) {
        return meta.activeMenu;
      }
      return path;
    },
    showLogo() {
      return SettingsModule.sidebarLogo;
    },
    variables() {
      return variables;
    },
    isCollapse() {
      return !this.sidebar.opened;
    },
  },
};
</script>

<style lang="scss" scoped>
.burger {
  display: flex;
  align-items: center;
  height: 56px;
  padding: 0 20px;
  justify-content: space-between;

  &:hover {
    background-color: #263445;
  }

  &.collapsed {
    padding: 0;
    justify-content: center;
  }

  &Text {
    color: rgb(191, 203, 217);
    line-height: 56px;
    font-size: 14px;
    white-space: nowrap;
    overflow: hidden;
  }
}
</style>
