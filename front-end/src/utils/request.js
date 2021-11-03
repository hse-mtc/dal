import axios from "axios";
import _debounce from "lodash/debounce";
import { Message } from "element-ui";
import { updateAccess } from "@/api/tokens";
import { AUTH_URLS } from "@/constants/api";
import router from "@/router";
import { UserModule } from "@/store";

const service = axios.create({
  baseURL: "/",
  timeout: 10000,
});

service.interceptors.request.use(
  config => {
    const token = UserModule.accessToken;
    if (token) {
      // eslint-disable-next-line no-param-reassign
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  error => Promise.reject(error),
);

service.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config;

    if (originalRequest.url.includes(AUTH_URLS.refresh)) {
      console.error("Не удалось обновить аксесс токен");
    } else if (originalRequest.url.includes(AUTH_URLS.obtain)) {
      Message({
        message: "Почта или пароль введены неверно, попробуйте еще раз",
        type: "error",
        duration: 5 * 1000,
      });

      console.error("Не удалось авторизоваться");
    } else if (error.response.status === 401) {
      const { refreshToken } = UserModule;

      try {
        if (refreshToken) {
          const { data } = await updateAccess({ refresh: refreshToken });
          UserModule.SET_TOKENS(data);

          return service(originalRequest);
        }

        console.error("Отсутствует рефреш токен");
      } catch (e) {
        console.error("Ошибка обновления токена:", e);
      }

      UserModule.RESET_TOKENS();

      const { name, fullPath } = router.currentRoute;
      const allowedPathsWithoutAuth = ["Login", "SignUp"];
      if (!allowedPathsWithoutAuth.includes(name)) {
        window.location.href = `/login?redirect=${fullPath}`;

        Message({
          message: "Ошибка авторизации",
          type: "error",
          duration: 5 * 1000,
        });
      }
    }

    throw error;
  },
);

export default service;
