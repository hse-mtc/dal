import { login, getInfo } from "@/api/user";
import { getToken, setToken, removeToken } from "@/utils/auth";
import { resetRouter } from "@/router";
import LocalStorageService from "../../utils/LocalStorageService";
const localStorageService = LocalStorageService.getService();

const state = {
  token: getToken(),
  name: "",
};

const mutations = {
  SET_TOKEN: (state, token) => {
    state.token = token;
  },
  SET_SURNAME: (state, surname) => {
    state.surname = surname;
  },
  SET_NAME: (state, name) => {
    state.name = name;
  },
  SET_PATRONYMIC: (state, patronymic) => {
    state.patronymic = patronymic;
  },
};

const actions = {
  // user login
  login({ commit }, userInfo) {
    const { username, password } = userInfo;
    return new Promise((resolve, reject) => {
      login({ username: username.trim(), password: password })
        .then((response) => {
          const { data } = response;
          commit("SET_TOKEN", data.access);
          setToken(data.access);
          localStorageService.setToken(data);
          resolve();
        })
        .catch((error) => {
          reject(error);
        });
    });
  },

  // get user info
  getInfo({ commit, state }) {
    return new Promise((resolve, reject) => {
      getInfo(state.token)
        .then((response) => {
          const { data } = response;

          if (!data) {
            reject("Verification failed, please Login again.");
          }

          const { surname, name, patronymic } = data;

          commit("SET_SURNAME", surname);
          commit("SET_NAME", name);
          commit("SET_PATRONYMIC", patronymic);

          resolve(data);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },

  // user logout
  logout({ commit }) {
    commit("SET_TOKEN", "");
    commit("SET_NAME", "");
    removeToken();
    resetRouter();
  },

  // set token
  setToken({ commit }, token) {
    return new Promise((resolve) => {
      commit("SET_TOKEN", token);
      setToken(token);
      localStorageService.setToken({ access: token, refresh: null });
      resolve();
    });
  },

  // remove token
  resetToken({ commit }) {
    return new Promise((resolve) => {
      commit("SET_TOKEN", "");
      removeToken();
      resolve();
    });
  },
};

export default {
  namespaced: true,
  state,
  mutations,
  actions,
};
