import request from "@/utils/request";
import { AUTH_URLS, BASE_API_URL, LMS_URLS } from "@/constants/api";

export function getUsers(params) {
  return request({
    url: BASE_API_URL + LMS_URLS.users.users,
    method: "get",
    params,
  });
}

export function getUserPermissions(params) {
  return request({
    url: BASE_API_URL + LMS_URLS.users.permissions,
    method: "get",
    params,
  });
}

export function getAllPermissions() {
  return request({
    url: BASE_API_URL + AUTH_URLS.permissions,
    method: "get",
  });
}

export function saveUserPermissions(id, roles) {
  return request({
    url: BASE_API_URL + `auth/users/${id}/permissions`,
    method: "post",
    data: { roles },
  });
}
