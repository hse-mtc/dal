import request from "@/utils/request";
import { AUTH_URLS, BASE_API_URL, LMS_URLS } from "@/constants/api";

export function login(data) {
  return request({
    url: BASE_API_URL + AUTH_URLS.obtain,
    method: "post",
    data,
  });
}

export function getUser() {
  return request({
    url: BASE_API_URL + AUTH_URLS.user,
    method: "get",
  });
}

export function changePassword(data) {
  return request({
    url: BASE_API_URL + AUTH_URLS.change_password,
    method: "post",
    data,
  });
}

export function registerStudent(data) {
  return request({
    url: BASE_API_URL + LMS_URLS.register.students,
    method: "post",
    data,
  });
}

export function registerTeacher(data) {
  return request({
    url: BASE_API_URL + LMS_URLS.register.teachers,
    method: "post",
    data,
  });
}
