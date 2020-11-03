import request from "@/utils/request";

export function getStudent(params) {
  return request({
    url: "/lms/student/",
    method: "get",
    params,
  });
}

export function postStudent(data) {
  return request({
    url: "/lms/student/",
    method: "post",
    data,
  });
}

export function patchStudent(data) {
  return request({
    url: `/lms/student/${data.id}/`,
    method: "patch",
    data,
  });
}

export function deleteStudent(id) {
  return request({
    url: `/lms/student/${id}/`,
    method: "delete",
  });
}
