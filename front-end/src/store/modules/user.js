import { login, getUser } from "@/api/user";
import { getToken, setToken, removeToken } from "@/utils/auth";

import { resetRouter } from "@/router";
import LocalStorageService from "../../utils/LocalStorageService";

const localStorageService = LocalStorageService.getService();

const initState = {
  token: getToken(),
  email: "",
  campuses: [],
};

const mutations = {
  /* eslint-disable no-param-reassign */
  SET_TOKEN: (state, token) => {
    state.token = token;
  },
  SET_EMAIL: (state, email) => {
    state.email = email;
  },
  SET_CAMPUSES: (state, campuses) => {
    state.campuses = campuses;
  },
  /* eslint-enable no-param-reassign */
};

const actions = {
  // user login
  login({ commit }, userInfo) {
    const { email, password } = userInfo;
    return new Promise((resolve, reject) => {
      login({ email: email.trim(), password })
        .then(response => {
          const { data } = response;
          commit("SET_TOKEN", data.access);
          setToken(data.access);
          localStorageService.setToken(data);
          resolve();
        })
        .catch(error => {
          reject(error);
        });
    });
  },

  // get user info
  getUser({ commit, state }) {
    return new Promise((resolve, reject) => {
      getUser(state.token)
        .then(response => {
          const { data } = response;
          if (!data) {
            reject(new Error("Verification failed, please Login again."));
          }

          const { email, campuses } = data;
          commit("SET_EMAIL", email);
          commit("SET_CAMPUSES", campuses);

          resolve(data);
        })
        .catch(error => {
          reject(error);
        });
    });
  },

  // user logout
  logout({ commit }) {
    commit("SET_TOKEN", "");
    commit("SET_EMAIL", "");
    removeToken();
    resetRouter();
  },

  // set token
  setToken({ commit }, token) {
    return new Promise(resolve => {
      commit("SET_TOKEN", token);
      setToken(token);
      localStorageService.setToken({ access: token, refresh: null });
      resolve();
    });
  },

  // remove token
  resetToken({ commit }) {
    return new Promise(resolve => {
      commit("SET_TOKEN", "");
      removeToken();
      resolve();
    });
  },
};

export default {
  namespaced: true,
  state: initState,
  mutations,
  actions,
};
