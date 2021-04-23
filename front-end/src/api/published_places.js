import request from "@/utils/request";
import { BASE_API_URL, DMS_URLS } from "@/constants/api";

export function getPublishPlaces(params) {
  return request({
    url: BASE_API_URL + DMS_URLS.publishers.publishers,
    method: "get",
    params,
  });
}

export function deletePublishPlaces(params) {
  return request({
    url: `${BASE_API_URL}${DMS_URLS.publishers.publishers}${params.id}/`,
    method: "delete",
  });
}

export function patchPublishPlaces(data) {
  return request({
    url: `${BASE_API_URL}${DMS_URLS.publishers.publishers}${data.id}/`,
    method: "patch",
    data,
  });
}

export function postPublishPlaces(data) {
  return request({
    url: `${BASE_API_URL}${DMS_URLS.publishers.publishers}`,
    method: "post",
    data,
  });
}
