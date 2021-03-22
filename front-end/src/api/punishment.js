import { BASE_API_URL, LMS_URLS } from "@/constants/api";
import request from "@/utils/request";

const {
  punishment: { punishment },
} = LMS_URLS;

export function getPunishment(params) {
  return request({
    url: BASE_API_URL + punishment,
    method: "get",
    params,
  });
}

export function patchPunishment(data) {
  data.student = { id: data.student.id };
  data.teacher = { id: data.teacher.id };
  return request({
    url: `${BASE_API_URL}${punishment}${data.id}/`,
    method: "patch",
    data,
  });
}

export function postPunishment(data) {
  return request({
    url: BASE_API_URL + punishment,
    method: "post",
    data,
  });
}

export function deletePunishment(params) {
  return request({
    url: `${BASE_API_URL}${punishment}${params.id}/`,
    method: "delete",
  });
}
