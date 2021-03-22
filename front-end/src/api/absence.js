import request from "@/utils/request";
import { LMS_URLS, BASE_API_URL } from "@/constants/api";

const {
  absence: { absence, journal },
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

export function patchAbsence(data) {
  if (data.studentid !== undefined) data.studentid = { id: data.studentid.id };
  return request({
    url: `${BASE_API_URL}${absence}${data.id}/`,
    method: "patch",
    data,
  });
}

export function postAbsence(data) {
  if (data.studentid !== undefined) data.studentid = { id: data.studentid.id };
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
