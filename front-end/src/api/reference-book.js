import request from "@/utils/request";
import { BASE_API_URL, LMS_URLS } from "@/constants/api";

export function getReferenceBooks(params) {
  return request({
    url: BASE_API_URL + LMS_URLS.reference.book,
    method: "get",
    params,
  });
}

export function getMilGroups() {
  return request({
    url: BASE_API_URL + LMS_URLS.reference.milgroups,
    method: "get",
  });
}

export function getMilFaculties() {
  return request({
    url: BASE_API_URL + LMS_URLS.reference.milfaculties,
    method: "get",
  });
}

export function getRanks() {
  return request({
    url: BASE_API_URL + LMS_URLS.reference.ranks,
    method: "get",
  });
}

export function getPosts() {
  return request({
    url: BASE_API_URL + LMS_URLS.reference.posts,
    method: "get",
  });
}
