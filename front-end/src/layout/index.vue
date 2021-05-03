<template>
  <div :class="classObj" class="app-wrapper">
    <div
      v-if="device === 'mobile' && sidebar.opened"
      class="drawer-bg"
      @click="handleClickOutside"
    />
    <Sidebar class="sidebar-container" />
    <div id="main-container" class="main-container">
      <div :class="{ 'fixed-header': fixedHeader }">
        <Navbar />
      </div>
      <AppMain />
    </div>
  </div>
</template>

<script>
import { mapActions } from "vuex";

import { getAuthors } from "@/api/authors";
import { getSubjects } from "@/api/subjects";
import { getPublishers } from "@/api/publishers";

import { Navbar, Sidebar, AppMain } from "./components";
import ResizeMixin from "./mixin/ResizeHandler";

export default {
  name: "Layout",
  components: {
    Navbar,
    Sidebar,
    AppMain,
  },
  mixins: [ResizeMixin],
  computed: {
    sidebar() {
      return this.$store.state.app.sidebar;
    },
    device() {
      return this.$store.state.app.device;
    },
    fixedHeader() {
      return this.$store.state.settings.fixedHeader;
    },
    classObj() {
      return {
        hideSidebar: !this.sidebar.opened,
        openSidebar: this.sidebar.opened,
        withoutAnimation: this.sidebar.withoutAnimation,
        mobile: this.device === "mobile",
      };
    },
  },
  mounted() {
    getAuthors()
      .then(response => {
        this.setAuthors(response.data);
      })
      .catch(() => {
        console.log("Данные по авторам не указаны");
      });
    getSubjects()
      .then(response => {
        this.setSubjects(response.data);
      })
      .catch(() => {
        console.log("Данные по предметам не указаны");
      });
    getPublishers()
      .then(response => {
        this.setPublishers(response.data);
      })
      .catch(() => {
        console.log("Данные по издательствам не указаны");
      });
  },
  methods: {
    ...mapActions({
      setAuthors: "documents/setAuthors",
      setSubjects: "subjects/setSubjects",
      setPublishers: "documents/setPublishers",
    }),
    handleClickOutside() {
      this.$store.dispatch("app/closeSideBar", { withoutAnimation: false });
    },
  },
};
</script>

<style lang="scss" scoped>
@import "~@/styles/mixin.scss";
@import "~@/styles/variables.scss";

.app-wrapper {
  @include clearfix;
  position: relative;
  height: 100%;
  width: 100%;

  &.mobile.openSidebar {
    position: fixed;
    top: 0;
  }
}

.drawer-bg {
  background: #000;
  opacity: 0.3;
  width: 100%;
  top: 0;
  height: 100%;
  position: absolute;
  z-index: 999;
}

.fixed-header {
  position: fixed;
  top: 0;
  right: 0;
  z-index: 9;
  width: calc(100% - #{$sideBarWidth});
  transition: width 0.28s;
}

.hideSidebar .fixed-header {
  width: calc(100% - 54px);
}

.mobile .fixed-header {
  width: 100%;
}
</style>
