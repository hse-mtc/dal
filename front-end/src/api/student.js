import request from "@/utils/request";
import { BASE_API_URL, LMS_URLS } from "@/constants/api";

const {
  stuff: { student },
} = LMS_URLS;

export function getStudent(params) {
  return request({
    url: BASE_API_URL + student,
    method: "get",
    params,
  });
}

export function postStudent(data) {
  // todo
  // eslint-disable-next-line no-param-reassign
  data.milgroup = { milgroup: data.milgroup.milgroup };
  return request({
    url: BASE_API_URL + student,
    method: "post",
    data,
  });
}

export function patchStudent(data) {
  return request({
    url: `${BASE_API_URL}${student}${data.id}/`,
    method: "patch",
    data,
  });
}

export function deleteStudent(id) {
  return request({
    url: `${BASE_API_URL}${student}${id}/`,
    method: "delete",
  });
}

export const updateStudentApplicationInfo = (id, data) => request({
  url: `${BASE_API_URL}${student}${id}/application/`,
  method: "PATCH",
  data,
});
