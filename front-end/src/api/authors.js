import request from "@/utils/request";
import { BASE_API_URL, DMS_URLS } from "@/constants/api";

export function getAuthors(params) {
  return request({
    url: BASE_API_URL + DMS_URLS.authors.authors,
    method: "get",
    params,
  });
}

export function deleteAuthors(params) {
  return request({
    url: `${BASE_API_URL}${DMS_URLS.authors.authors}${params.id}/`,
    method: "delete",
  });
}

export function patchAuthor(data) {
  return request({
    url: `${BASE_API_URL}${DMS_URLS.authors.authors}${data.id}/`,
    method: "patch",
    data,
  });
}

export function postAuthor(data) {
  return request({
    url: `${BASE_API_URL}${DMS_URLS.authors.authors}`,
    method: "post",
    data,
  });
}
