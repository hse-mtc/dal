import request from "@/utils/request";
import { AUTH_URLS, BASE_API_URL } from "@/constants/api";

export function login(data) {
  return request({
    url: BASE_API_URL + AUTH_URLS.obtain,
    method: "post",
    data,
  });
}

export function getInfo() {
  return request({
    url: BASE_API_URL + AUTH_URLS.info,
    method: "get",
  });
}

export function createPassword(data) {
  return request({
    url: BASE_API_URL + AUTH_URLS.create_password,
    method: "post",
    data
  })
}
