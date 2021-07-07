import request from "@/utils/request";
import { BASE_API_URL, DMS_URLS } from "@/constants/api";

export function getPublishers(params) {
  return request({
    url: BASE_API_URL + DMS_URLS.publishers.publishers,
    method: "get",
    params,
  });
}

export function editPublisher(id, data) {
  return request({
    url: `${BASE_API_URL}${DMS_URLS.publishers.publishers}${id}/`,
    method: "PATCH",
    data,
  });
}

export function deletePublisher(id) {
  return request({
    url: `${BASE_API_URL}${DMS_URLS.publishers.publishers}${id}/`,
    method: "DELETE",
  });
}

export function addPublisher(name) {
  return request({
    url: `${BASE_API_URL}${DMS_URLS.publishers.publishers}`,
    method: "POST",
    data: { name },
  });
}
