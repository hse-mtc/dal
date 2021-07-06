import {
  VuexModule,
  Module,
  Mutation,
  Action,
} from "vuex-module-decorators";

import store, { UserModule } from "@/store";

import { login, getUser } from "@/api/user";
import { getToken, setToken, removeToken } from "@/utils/auth";

import { resetRouter } from "@/router";
import { getError } from "@/utils/message";
import LocalStorageService from "../../utils/LocalStorageService";

const localStorageService = LocalStorageService.getService();

@Module({ store, name: "user", namespaced: true })
class User extends VuexModule {
  token = getToken();
  _email = "";
  _campuses = [];
  _personType = "";
  _personId = 0;
  _userInfoLoaded = false;

  @Mutation
  SET_IS_LOADED(value) {
    this._userInfoLoaded = value;
  }

  @Mutation
  SET_TOKEN(token) {
    this.token = token;
  }

  @Mutation
  SET_EMAIL(email) {
    this._email = email;
  }

  @Mutation
  SET_CAMPUSES(campuses) {
    this._campuses = campuses;
  }

  @Mutation
  SET_PERSON_TYPE(type) {
    this._personType = type;
  }

  @Mutation
  SET_PERSON_ID(id) {
    this._personId = id;
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
    try {
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
      this.SET_IS_LOADED(true);
    } catch (err) {
      getError("информации о пользователе", err.response.status);
    }
  }

  @Action
  logout() {
    this.SET_TOKEN();
    this.SET_EMAIL();
    this.SET_CAMPUSES([]);
    this.SET_PERSON_TYPE("");
    this.SET_PERSON_ID(0);
    this.SET_IS_LOADED(false);
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

  get email() {
    if (!this._userInfoLoaded) {
      UserModule.getUser();
    }

    return this._email;
  }

  get campuses() {
    if (!this._userInfoLoaded) {
      UserModule.getUser();
    }

    return this._campuses;
  }

  get personType() {
    if (!this._userInfoLoaded) {
      UserModule.getUser();
    }

    return this._personType;
  }

  get personId() {
    if (!this._userInfoLoaded) {
      UserModule.getUser();
    }

    return this._personId;
  }
}

export default User;
