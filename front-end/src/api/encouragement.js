import request from "@/utils/request";
import { BASE_API_URL, LMS_URLS } from "@/constants/api";

const {
  encouragement: { encouragement },
} = LMS_URLS;

export function getEncouragement(params) {
  return request({
    url: BASE_API_URL + encouragement,
    method: "get",
    params,
  });
}

export function patchEncouragement(data) {
  return request({
    url: `${BASE_API_URL}${encouragement}${data.id}/`,
    method: "patch",
    data,
  });
}

export function postEncouragement(data) {
  return request({
    url: BASE_API_URL + encouragement,
    method: "post",
    data,
  });
}

export function deleteEncouragement(params) {
  return request({
    url: `${BASE_API_URL}${encouragement}${params.id}/`,
    method: "delete",
  });
}
