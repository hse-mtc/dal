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
        <el-menu-item
          class="sidebar-close-button"
          @click="close"
        >
          <i class="el-icon-back" />
          Свернуть
        </el-menu-item>

        <el-menu-item class="user-controls-wrapper">
          <el-dropdown class="user-controls" trigger="click">
            <div class="avatar-wrapper m-0" style="font-size: 19px">
              <!--          <img :src="avatar+'?imageView2/1/w/80/h/80'" class="user-avatar">-->
              {{ email }}
              <i class="el-icon-caret-bottom" />
            </div>
            <el-dropdown-menu slot="dropdown" class="user-dropdown">
              <router-link to="/">
                <el-dropdown-item> Домой </el-dropdown-item>
              </router-link>
              <el-dropdown-item v-if="personType && personId">
                <span style="display: block" @click="profile">Мой профиль</span>
              </el-dropdown-item>
              <el-dropdown-item divided>
                <span style="display: block" @click="logout">Выход</span>
              </el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
        </el-menu-item>

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
import { AppModule, SettingsModule, UserModule } from "@/store";
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
    email() {
      return UserModule.email;
    },
    personType() {
      return UserModule.personType;
    },
  },
  methods: {
    profile() {
      if (this.personType && this.personId) {
        const name = this.personType.charAt(0).toUpperCase() + this.personType.slice(1);
        this.$router.push({
          name,
          params: { [`${this.personType}Id`]: this.personId },
        });
      }
    },
    logout() {
      UserModule.logout();
      window.location.href = "/login";
    },
    close() {
      AppModule.closeSideBar({ withoutAnimation: false });
    },
  },
};
</script>

<style lang="scss" scoped>
.sidebar-close-button {
  display: none;

  @media screen and (max-width: 992px) {
    display: block;
  }
}

.user-controls {
  display: flex;
  justify-content: center;
  color: #000;
  background-color: #dfdfdf;
  border-radius: 20px;

  &-wrapper {
    display: none;

    @media screen and (max-width: 499px) {
      display: block;
    }
  }

}

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
    color: #bfcbd9;
    line-height: 56px;
    font-size: 14px;
    white-space: nowrap;
    overflow: hidden;
  }
}
</style>
