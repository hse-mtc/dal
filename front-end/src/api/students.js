import request from "@/utils/request";
import { BASE_API_URL, LMS_URLS } from "@/constants/api";

const {
  stuff: { students },
} = LMS_URLS;

export function getStudent(params) {
  return request({
    url: BASE_API_URL + students,
    method: "get",
    params,
  });
}

export function postStudent(data) {
  return request({
    url: BASE_API_URL + students,
    method: "post",
    data,
  });
}

export function patchStudent(data) {
  return request({
    url: `${BASE_API_URL}${students}${data.id}/`,
    method: "patch",
    data,
  });
}

export function deleteStudent(id) {
  return request({
    url: `${BASE_API_URL}${students}${id}/`,
    method: "delete",
  });
}
