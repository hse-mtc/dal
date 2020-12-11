import request from "@/utils/request";

export function getEncouragement(params) {
  return request({
    url: "/lms/encouragement/",
    method: "get",
    params,
  });
}

export function patchEncouragement(data) {
  data.student = { id: data.student.id };
  data.teacher = { id: data.teacher.id };
  return request({
    url: `/lms/encouragement/${data.id}/`,
    method: "patch",
    data,
  });
}

export function postEncouragement(data) {
  return request({
    url: `/lms/encouragement/`,
    method: "post",
    data,
  });
}

export function deleteEncouragement(params) {
  return request({
    url: `/lms/encouragement/${params.id}/`,
    method: "delete",
  });
}
