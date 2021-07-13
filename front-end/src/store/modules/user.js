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
  accessToken = tokenService.access;
  refreshToken = tokenService.refresh;
  userId = tokenService.userId;
  _email = "";
  _permissions = [];
  _campuses = [];
  _person = {};
  _isSuperuser = false;
  _userInfoLoaded = false;

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
  SET_PERSON(person) {
    this._person = person;
  }

  @Mutation
  SET_IS_SUPERUSER(isSuperuser) {
    this._isSuperuser = isSuperuser;
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
        email, campuses, person, all_permissions: permissions, is_superuser: isSuperuser,
      } = data;

      this.SET_EMAIL(email);
      this.SET_CAMPUSES(campuses);
      this.SET_PERMISSIONS(permissions);
      this.SET_PERSON(person);
      this.SET_IS_SUPERUSER(isSuperuser);
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
    this.SET_PERSON({});
    this.SET_USER_ID(null);
    this.SET_PERMISSIONS([]);
    this.SET_IS_SUPERUSER(false);
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

  get isSuperuser() {
    if (!this._userInfoLoaded) {
      UserModule.getUser();
    }

    return this._isSuperuser;
  }

  get personType() {
    if (!this._userInfoLoaded) {
      UserModule.getUser();
    }

    return this._person.type;
  }

  get personId() {
    if (!this._userInfoLoaded) {
      UserModule.getUser();
    }

    return this._person.id;
  }

  get personMilgroups() {
    if (!this._userInfoLoaded) {
      UserModule.getUser();
    }

    return this._person.milgroups;
  }

  get personMilfaculty() {
    if (!this._userInfoLoaded) {
      UserModule.getUser();
    }

    return this._person.milfaculty;
  }
}

export default User;
