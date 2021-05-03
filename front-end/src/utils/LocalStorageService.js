import jwtDecode from "jwt-decode";
import store from "../store";

const LocalStorageService = (function serviceConstructor() {
  let service;

  function getService() {
    if (!service) {
      service = this;
    }
    return service;
  }

  function setToken(tokenObj) {
    localStorage.setItem("access_token", tokenObj.access);
    localStorage.setItem("refresh_token", tokenObj.refresh);
  }

  function getAccessToken() {
    const token = localStorage.getItem("access_token");
    if (token) {
      const decoded = jwtDecode(token);
      store.dispatch("app/setUserId", decoded.user_id);
    }
    return token;
  }

  function getRefreshToken() {
    return localStorage.getItem("refresh_token");
  }

  function clearToken() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
  }

  return {
    getService,
    setToken,
    getAccessToken,
    getRefreshToken,
    clearToken,
  };
}());

export default LocalStorageService;
