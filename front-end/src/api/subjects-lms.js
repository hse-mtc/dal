import request from "@/utils/request";
import { BASE_API_URL, LMS_URLS } from "@/constants/api";

const {
  subject: { subject },
} = LMS_URLS;

export function getSubjects(params) {
  return request({
    url: BASE_API_URL + subject,
    method: "get",
    params,
  });
}

export function findSubject(params) {
  return request({
    url: `${BASE_API_URL}${subject}${params.id}/`,
    method: "get",
  });
}

export function deleteSubject(id) {
  return request({
    url: `${BASE_API_URL}${subject}${id}/`,
    method: "delete",
  });
}
