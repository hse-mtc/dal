import defaultSettings from "@/settings";

const { showSettings, fixedHeader, sidebarLogo } = defaultSettings;

const initState = {
  showSettings,
  fixedHeader,
  sidebarLogo,
};

const mutations = {
  CHANGE_SETTING: (state, { key, value }) => {
    // eslint-disable-next-line no-prototype-builtins
    if (state.hasOwnProperty(key)) {
      // eslint-disable-next-line no-param-reassign
      state[key] = value;
    }
  },
};

const actions = {
  changeSetting({ commit }, data) {
    commit("CHANGE_SETTING", data);
  },
};

export default {
  namespaced: true,
  state: initState,
  mutations,
  actions,
};
