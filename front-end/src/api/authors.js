import request from "@/utils/request";
import { BASE_API_URL, DMS_URLS } from "@/constants/api";

const { authors: { authors } } = DMS_URLS;

export function getAuthors(params) {
  return request({
    url: BASE_API_URL + authors,
    method: "get",
    params,
  });
}

export function editAuthors(id, data) {
  return request({
    url: `${BASE_API_URL}${authors}${id}/`,
    method: "PATCH",
    data,
  });
}

export function deleteAuthor(id) {
  return request({
    url: `${BASE_API_URL}${authors}${id}/`,
    method: "DELETE",
  });
}

export function addAuthor(data) {
  return request({
    url: `${BASE_API_URL}${authors}`,
    method: "POST",
    data,
  });
}
