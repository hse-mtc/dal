import request from "@/utils/request";
import { BASE_API_URL, LMS_URLS } from "@/constants/api";

const {
  staff: { teachers },
} = LMS_URLS;

export function getTeacher(params) {
  return request({
    url: BASE_API_URL + teachers,
    method: "get",
    params,
  });
}

export function findTeacher(id) {
  return request({
    url: `${BASE_API_URL}${teachers}${id}/`,
    method: "get",
  });
}

export function postTeacher(data) {
  return request({
    url: BASE_API_URL + teachers,
    method: "post",
    data,
  });
}

export function patchTeacher(data) {
  return request({
    url: `${BASE_API_URL}${teachers}${data.id}/`,
    method: "patch",
    data,
  });
}

export function deleteTeacher(id) {
  return request({
    url: `${BASE_API_URL}${teachers}${id}/`,
    method: "delete",
  });
}
