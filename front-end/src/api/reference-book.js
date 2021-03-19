import request from "@/utils/request";
import { BASE_API_URL, LMS_URLS } from "@/constants/api";

export function getReferenceBooks(params) {
  return request({
    url: BASE_API_URL + LMS_URLS.reference.book,
    method: "get",
    params,
  });
}

export function getReferenceMilSpecialties(params) {
  return request({
    url: BASE_API_URL + LMS_URLS.reference.milspecialties,
    method: "get",
    params,
  });
}
