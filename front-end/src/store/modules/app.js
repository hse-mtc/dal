import {
  VuexModule,
  Module,
  Mutation,
  Action,
} from "vuex-module-decorators";
import Cookies from "js-cookie";

import store from "@/store";

@Module({ store, name: "app", namespaced: true })
class App extends VuexModule {
  sidebar = {
    opened: Cookies.get("sidebarStatus")
      ? !!+Cookies.get("sidebarStatus")
      : true,
    withoutAnimation: false,
  }

  device= "desktop"
  userId = ""

  @Mutation
  TOGGLE_SIDEBAR() {
    this.sidebar.opened = !this.sidebar.opened;
    this.sidebar.withoutAnimation = false;
    if (this.sidebar.opened) {
      Cookies.set("sidebarStatus", 1);
    } else {
      Cookies.set("sidebarStatus", 0);
    }
  }

  @Mutation
  CLOSE_SIDEBAR(withoutAnimation) {
    Cookies.set("sidebarStatus", 0);
    this.sidebar.opened = false;
    this.sidebar.withoutAnimation = withoutAnimation;
  }

  @Mutation
  TOGGLE_DEVICE(device) {
    this.device = device;
  }

  @Mutation
  SET_USER_ID(payload) {
    this.userId = payload;
  }

  @Action({ commit: "SET_USER_ID" })
  setUserId(userId) {
    return userId;
  }

  @Action()
  toggleSideBar() {
    this.TOGGLE_SIDEBAR();
  }

  @Action({ commit: "CLOSE_SIDEBAR" })
  closeSideBar({ withoutAnimation }) {
    return withoutAnimation;
  }

  @Action({ commit: "TOGGLE_DEVICE" })
  toggleDevice(device) {
    return device;
  }
}

export default App;
