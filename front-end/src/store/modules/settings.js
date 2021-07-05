import {
  VuexModule,
  Module,
  Mutation,
  Action,
} from "vuex-module-decorators";

import store from "@/store";
import defaultSettings from "@/settings";

const { showSettings, fixedHeader, sidebarLogo } = defaultSettings;

@Module({ store, name: "settings", namespaced: true })
class Settings extends VuexModule {
  showSettings = showSettings
  fixedHeader = fixedHeader
  sidebarLogo = sidebarLogo

  @Mutation
  CHANGE_SETTING({ key, value }) {
    // eslint-disable-next-line no-prototype-builtins
    if (this.hasOwnProperty(key)) {
      this[key] = value;
    }
  }

  @Action({ commit: "CHANGE_SETTING" })
  changeSetting(data) {
    return data;
  }
}

export default Settings;
