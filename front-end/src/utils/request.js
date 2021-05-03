import axios from "axios";
import { Message } from "element-ui";
import { updateAccess } from "@/api/tokens";
import LocalStorageService from "./LocalStorageService";

const localStorageService = LocalStorageService.getService();

// create an axios instance
const service = axios.create({
  baseURL: "/",
  timeout: 10000, // request timeout
  // withCredentials: true, // send cookies when cross-domain requests
});

// request interceptor
service.interceptors.request.use(
  config => {
    const token = localStorageService.getAccessToken();
    if (token) {
      // eslint-disable-next-line no-param-reassign
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  error => {
    console.log(error); // for debug
    return Promise.reject(error);
  },
);

// response interceptor
service.interceptors.response.use(
  /**
   * If you want to get http information such as headers or status
   * Please return  response => response
   */

  /**
   * Determine the request status by custom code
   * Here is just an example
   * You can also judge the status by HTTP Status Code
   */
  response => response,
  error => {
    console.log(`err${error}`); // for debug
    const originalRequest = error.config;
    if (
      error.response.status === 401
      // eslint-disable-next-line no-underscore-dangle
      && !originalRequest._retry
      && !originalRequest.url.includes("tokens/refresh")
      && !originalRequest.url.includes("tokens/obtain")
    ) {
      // eslint-disable-next-line no-underscore-dangle
      originalRequest._retry = true;
      const refreshToken = localStorageService.getRefreshToken();
      return updateAccess({
        refresh: refreshToken,
      })
        .then(res => {
          if (res.status === 200) {
            localStorageService.setToken(res.data);
            axios.defaults.headers.common.Authorization = `Bearer ${res.data.access}`;
            originalRequest.headers.Authorization = `Bearer ${res.data.access}`;
            return axios(originalRequest);
          }

          throw new Error();
        })
        .catch(() => {
          localStorageService.clearToken();
          window.location.reload();
        });
    }

    if (
      error.response.status === 401
      && originalRequest.url.includes("tokens/obtain")
    ) {
      Message({
        message: "Логин или пароль введены неверно, попробуйте еще раз",
        type: "error",
        duration: 5 * 1000,
      });
    } else {
      Message({
        message: error.response.data.detail || error.message,
        type: "error",
        duration: 5 * 1000,
      });
    }

    return Promise.reject(error);
  },
);

export default service;
