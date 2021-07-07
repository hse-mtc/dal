import {
  VuexModule,
  Module,
  Mutation,
  Action,
} from "vuex-module-decorators";

import store, { UserModule } from "@/store";

import { login, getUser } from "@/api/user";

import { resetRouter } from "@/router";
import { tokenService } from "../../utils/tokenService";

@Module({ store, name: "user", namespaced: true })
class User extends VuexModule {
  accessToken = tokenService.access
  refreshToken = tokenService.refresh
  userId = tokenService.userId
  _email = ""
  _campuses = []
  _userInfoLoaded = false

  @Mutation
  SET_IS_LOADED(value) {
    this._userInfoLoaded = value;
  }

  @Mutation
  SET_TOKENS({ access, refresh }) {
    this.accessToken = access;
    this.refreshToken = refresh;

    tokenService.setTokens({ access, refresh });
  }

  @Mutation
  RESET_TOKENS() {
    this.accessToken = "";
    this.refreshToken = "";

    tokenService.clearTokens();
  }

  @Mutation
  SET_USER_ID(userId) {
    this.userId = userId;
  }

  @Mutation
  SET_EMAIL(email) {
    this._email = email;
  }

  @Mutation
  SET_CAMPUSES(campuses) {
    this._campuses = campuses;
  }

  @Action
  async login(userInfo) {
    const { email, password } = userInfo;

    try {
      const { data } = await login({ email: email.trim(), password });
      this.SET_TOKENS(data);
      this.SET_USER_ID(tokenService.userId);
      return true;
    } catch (e) {
      console.log("Не удалось авторизоваться", e);
      return false;
    }
  }

  @Action
  async getUser() {
    try {
      const { data } = await getUser(this.token);
      const { email, campuses } = data;
      this.SET_EMAIL(email);
      this.SET_CAMPUSES(campuses);
      this.SET_IS_LOADED(true);
    } catch (e) {
      console.error("Не удалось получить данные пользователя", e);
    }
  }

  @Action
  logout() {
    this.RESET_TOKENS();
    this.SET_EMAIL("");
    this.SET_CAMPUSES([]);
    this.SET_USER_ID(null);
    this.SET_IS_LOADED(false);
  }

  get email() {
    if (!this._userInfoLoaded && this.accessToken) {
      UserModule.getUser();
    }

    return this._email;
  }

  get campuses() {
    if (!this._userInfoLoaded && this.accessToken) {
      UserModule.getUser();
    }

    return this._campuses;
  }
}

export default User;
