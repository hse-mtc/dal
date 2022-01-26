import request from "@/utils/request";
import { LMS_URLS, BASE_API_URL } from "@/constants/api";

const {
  absence: { absence, journal, attachment },
} = LMS_URLS;

export function getAbsence(params) {
  return request({
    url: BASE_API_URL + absence,
    method: "get",
    params,
  });
}

export function getAbsenceJournal(params) {
  return request({
    url: BASE_API_URL + journal,
    method: "get",
    params,
  });
}

export function patchAbsence(id, data) {
  return request({
    url: `${BASE_API_URL}${absence}${id}/`,
    method: "patch",
    data,
  });
}

export function deleteAbsenceAttachment(id) {
  return request({
    url: `${BASE_API_URL}${attachment}${id}/`,
    method: "delete",
  });
}

export function postAbsence(data) {
  // todo
  // eslint-disable-next-line no-param-reassign
  if (data.studentid !== undefined) { data.studentid = { id: data.studentid.id }; }
  return request({
    url: BASE_API_URL + absence,
    method: "post",
    data,
  });
}

export function deleteAbsence(params) {
  return request({
    url: `${BASE_API_URL}${absence}${params.id}/`,
    method: "delete",
  });
}
