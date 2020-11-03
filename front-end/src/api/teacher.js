import request from "@/utils/request";

export function getTeacher(params) {
  return request({
    url: "/lms/teacher/",
    method: "get",
    params,
  });
}

export function postTeacher(data) {
  return request({
    url: "/lms/teacher/",
    method: "post",
    data,
  });
}

export function patchTeacher(data) {
  return request({
    url: `/lms/teacher/${data.id}/`,
    method: "patch",
    data,
  });
}

export function deleteTeacher(id) {
  return request({
    url: `/lms/teacher/${id}/`,
    method: "delete",
  });
}
