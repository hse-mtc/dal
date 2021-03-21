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

export function getReferenceMilSpecialties(params) {
  return request({
    url: BASE_API_URL + milspecialties,
    method: "get",
    params,
  });
}
