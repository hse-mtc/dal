import request from "@/utils/request";
import { BASE_API_URL, LMS_URLS } from "@/constants/api";

const { stuff: { teacher } } = LMS_URLS

export function getTeacher(params) {
  return request({
    url: BASE_API_URL + teacher,
    method: "get",
    params,
  });
}

export function postTeacher(data) {
  return request({
    url: BASE_API_URL + teacher,
    method: "post",
    data,
  });
}

export function patchTeacher(data) {
  return request({
    url: `${BASE_API_URL}${teacher}${data.id}/`,
    method: "patch",
    data,
  });
}

export function deleteTeacher(id) {
  return request({
    url: `${BASE_API_URL}${teacher}${id}/`,
    method: "delete",
  });
}
