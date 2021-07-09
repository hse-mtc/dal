import {
  VuexModule,
  Module,
  Mutation,
  Action,
} from "vuex-module-decorators";

import store, { UserModule } from "@/store";

import { login, getUser } from "@/api/user";

import { getError } from "@/utils/message";
import { tokenService } from "../../utils/tokenService";

@Module({ store, name: "user", namespaced: true })
class User extends VuexModule {
  accessToken = tokenService.access
  refreshToken = tokenService.refresh
  userId = tokenService.userId
  _email = ""
  _permissions = []
  _campuses = []
  _personType = "";
  _personId = 0;
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

  @Mutation
  SET_PERMISSIONS(permissions) {
    this._permissions = permissions;
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

      if (!data) {
        throw new Error("Verification failed, please Login again.");
      }

      const {
        // eslint-disable-next-line camelcase
        email, campuses, person_type, person_id, all_permissions: permissions,
      } = data;

      this.SET_EMAIL(email);
      this.SET_CAMPUSES(campuses);
      this.SET_PERMISSIONS(permissions);
      this.SET_PERSON_TYPE(person_type);
      this.SET_PERSON_ID(person_id);
      this.SET_IS_LOADED(true);
    } catch (err) {
      getError("информации о пользователе", err.response.status);
    }
  }

  @Action
  logout() {
    this.RESET_TOKENS();
    this.SET_EMAIL("");
    this.SET_CAMPUSES([]);
    this.SET_PERSON_TYPE("");
    this.SET_PERSON_ID(0);
    this.SET_USER_ID(null);
    this.SET_PERMISSIONS([]);
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

  get permissions() {
    if (!this._userInfoLoaded) {
      UserModule.getUser();
    }

    return this._permissions;
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
