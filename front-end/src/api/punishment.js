import request from "@/utils/request";

export function getPunishment(params) {
  return request({
    url: "/lms/punishment/",
    method: "get",
    params,
  });
}

export function patchPunishment(data) {
  data.student = { id: data.student.id };
  data.teacher = { id: data.teacher.id };
  return request({
    url: `/lms/punishment/${data.id}/`,
    method: "patch",
    data,
  });
}

export function postPunishment(data) {
  return request({
    url: `/lms/punishment/`,
    method: "post",
    data,
  });
}

export function deletePunishment(params) {
  return request({
    url: `/lms/punishment/${params.id}/`,
    method: "delete",
  });
}
