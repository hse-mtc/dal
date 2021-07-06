import request from "@/utils/request";
import { LMS_URLS, BASE_API_URL } from "@/constants/api";

const {
  achievement: { achievement },
} = LMS_URLS;

export function getAchievement(params) {
  return request({
    url: BASE_API_URL + achievement,
    method: "get",
    params,
  });
}

export function patchAchievement(data) {
  return request({
    url: `${BASE_API_URL}${achievement}${data.id}/`,
    method: "patch",
    data,
  });
}

export function postAchievement(data) {
  return request({
    url: BASE_API_URL + achievement,
    method: "post",
    data,
  });
}

export function deleteAchievement(id) {
  return request({
    url: `${BASE_API_URL}${achievement}${id}/`,
    method: "delete",
  });
}
