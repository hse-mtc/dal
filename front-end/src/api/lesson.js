import request from "@/utils/request";
import { BASE_API_URL, LMS_URLS } from "@/constants/api";

const {
  lessons: { lesson, journal },
} = LMS_URLS;

export function getLesson(params) {
  return request({
    url: BASE_API_URL + lesson,
    method: "get",
    params,
  });
}

export function getLessonJournal(params) {
  return request({
    url: BASE_API_URL + journal,
    method: "get",
    params,
  });
}

export function patchLesson(data) {
  return request({
    url: `${BASE_API_URL}${lesson}${data.id}/`,
    method: "patch",
    data,
  });
}

export function postLesson(data) {
  return request({
    url: BASE_API_URL + lesson,
    method: "post",
    data,
  });
}

export function deleteLesson(params) {
  return request({
    url: `${BASE_API_URL}${lesson}${params.id}/`,
    method: "delete",
  });
}
