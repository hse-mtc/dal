import request from "@/utils/request";

export function getMark(params) {
  return request({
    url: "/lms/mark/",
    method: "get",
    params,
  });
}

export function getMarkJournal(params) {
  return request({
    url: "/lms/mark-journal/",
    method: "get",
    params,
  });
}

export function patchMark(data) {
  return request({
    url: `/lms/mark/${data.id}/`,
    method: "patch",
    data,
  });
}

export function postMark(data) {
  return request({
    url: `/lms/mark/`,
    method: "post",
    data,
  });
}

export function deleteMark(params) {
  return request({
    url: `/lms/mark/${params.id}/`,
    method: "delete",
  });
}
