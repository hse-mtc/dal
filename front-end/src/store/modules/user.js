import {
  VuexModule,
  Module,
  Mutation,
  Action,
} from "vuex-module-decorators";

import store from "@/store";

import { login, getUser } from "@/api/user";
import { getToken, setToken, removeToken } from "@/utils/auth";

import { resetRouter } from "@/router";
import LocalStorageService from "../../utils/LocalStorageService";

const localStorageService = LocalStorageService.getService();

@Module({ store, name: "user", namespaced: true })
class User extends VuexModule {
  token = getToken();
  email = "";
  campuses = [];
  personType = "";
  personId = 0;

  @Mutation
  SET_TOKEN(token) {
    this.token = token;
  }

  @Mutation
  SET_EMAIL(email) {
    this.email = email;
  }

  @Mutation
  SET_CAMPUSES(campuses) {
    this.campuses = campuses;
  }

  @Mutation
  SET_PERSON_TYPE(type) {
    this.personType = type;
  }

  @Mutation
  SET_PERSON_ID(id) {
    this.personId = id;
  }

  @Action
  async login(userInfo) {
    const { email, password } = userInfo;

    const { data } = await login({ email: email.trim(), password });
    this.SET_TOKEN(data.access);
    setToken(data.access);
    localStorageService.setToken(data);
  }

  @Action
  async getUser() {
    const { data } = await getUser(this.token);

    if (!data) {
      throw new Error("Verification failed, please Login again.");
    }

    const {
      // eslint-disable-next-line camelcase
      email, campuses, person_type, person_id,
    } = data;
    this.SET_EMAIL(email);
    this.SET_CAMPUSES(campuses);
    this.SET_PERSON_TYPE(person_type);
    this.SET_PERSON_ID(person_id);
  }

  @Action
  logout() {
    this.SET_TOKEN();
    this.SET_EMAIL();
    removeToken();
    resetRouter();
  }

  @Action
  async setToken(token) {
    this.SET_TOKEN(token);
    setToken(token);
    localStorageService.setToken({ access: token, refresh: null });
  }

  @Action
  async resetToken() {
    this.SET_TOKEN("");
    removeToken();
  }
}

export default User;
