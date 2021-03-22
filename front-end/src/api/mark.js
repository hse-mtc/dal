import request from "@/utils/request";
import { BASE_API_URL, LMS_URLS } from "@/constants/api";

const {
  marks: { mark, journal },
} = LMS_URLS;

export function getMark(params) {
  return request({
    url: BASE_API_URL + mark,
    method: "get",
    params,
  });
}

export function getMarkJournal(params) {
  return request({
    url: BASE_API_URL + journal,
    method: "get",
    params,
  });
}

export function patchMark(data) {
  return request({
    url: `${BASE_API_URL}${mark}${data.id}/`,
    method: "patch",
    data,
  });
}

export function postMark(data) {
  return request({
    url: BASE_API_URL + mark,
    method: "post",
    data,
  });
}

export function deleteMark(params) {
  return request({
    url: `${BASE_API_URL}${mark}${params.id}/`,
    method: "delete",
  });
}
