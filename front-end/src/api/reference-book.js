import request from "@/utils/request";
import { BASE_API_URL, LMS_URLS } from "@/constants/api";

const {reference: {book, milspecialties}} = LMS_URLS

export function getReferenceBooks(params) {
  return request({
    url: BASE_API_URL + book,
    method: "get",
    params,
  });
}

export function getReferenceMilSpecialties(campus) {
  return request({
    url: BASE_API_URL + milspecialties,
    method: "get",
    params: {campus},
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
