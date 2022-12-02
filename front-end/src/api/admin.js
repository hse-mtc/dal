import request from "@/utils/request";
import { AUTH_URLS, BASE_API_URL, LMS_URLS } from "@/constants/api";

export function getUsers(params) {
  return request({
    url: BASE_API_URL + LMS_URLS.users.users,
    method: "get",
    params,
  });
}

export function getUserPermissions(id) {
  return request({
    url: `${BASE_API_URL}${AUTH_URLS.userControl}${id}/`,
    method: "get",
  });
}

export function getRolePermissions(id) {
  return request({
    url: `${BASE_API_URL}${AUTH_URLS.roles}${id}/`,
    method: "get",
  });
}

export function getAllPermissions() {
  return request({
    url: BASE_API_URL + AUTH_URLS.permissions,
    method: "get",
  });
}

export function getAllRoles() {
  return request({
    url: BASE_API_URL + AUTH_URLS.roles,
    method: "get",
  });
}

export function addRole(data) {
  return request({
    url: BASE_API_URL + AUTH_URLS.roles,
    method: "post",
    data,
  });
}

export function deleteRole(id) {
  return request({
    url: `${BASE_API_URL}${AUTH_URLS.roles}${id}/`,
    method: "delete",
  });
}

export function saveUserControl(id, data) {
  return request({
    url: `${BASE_API_URL}${AUTH_URLS.userControl}${id}/`,
    method: "patch",
    data,
  });
}

export function saveRoleChanges(id, data) {
  return request({
    url: `${BASE_API_URL}${AUTH_URLS.roles}${id}/`,
    method: "patch",
    data,
  });
}

export function getTeachersToApprove() {
  return request({
    url: BASE_API_URL + LMS_URLS.staff.teachersApprovals,
    method: "get",
  });
}

export function getStudentsToApprove() {
  return request({
    url: BASE_API_URL + LMS_URLS.staff.studentsApprovals,
    method: "get",
  });
}

export function approveTeacher(id, data) {
  return request({
    url: `${BASE_API_URL + LMS_URLS.staff.teachersApprovals}${id}/`,
    method: "patch",
    data,
  });
}

export function approveStudent(id, data) {
  return request({
    url: `${BASE_API_URL + LMS_URLS.staff.studentsApprovals}${id}/`,
    method: "patch",
    data,
  });
}

export function disapproveStudent(id) {
  return request({
    url: `${BASE_API_URL + LMS_URLS.staff.students}${id}/`,
    method: "delete",
  });
}

export function disapproveTeacher(id) {
  return request({
    url: `${BASE_API_URL + LMS_URLS.staff.teachers}${id}/`,
    method: "delete",
  });
}
