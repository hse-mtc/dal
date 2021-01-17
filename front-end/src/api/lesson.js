import request from "@/utils/request";

export function getLesson(params) {
  return request({
    url: "/lms/lesson/",
    method: "get",
    params,
  });
}

export function getLessonJournal(params) {
  return request({
    url: "/lms/lesson-journal/",
    method: "get",
    params,
  });
}

export function patchLesson(data) {
  return request({
    url: `/lms/lesson/${data.id}/`,
    method: "patch",
    data,
  });
}

export function postLesson(data) {
  return request({
    url: `/lms/lesson/`,
    method: "post",
    data,
  });
}

export function deleteLesson(params) {
  return request({
    url: `/lms/lesson/${params.id}/`,
    method: "delete",
  });
}
