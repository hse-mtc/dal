import request from "@/utils/request";

export function getTopics(id) {
  return request({
    url: `/dms/sections/${id}`,
    method: "get",
  });
}

export function addTopics(data) {
  return request({
    url: `/dms/topics/`,
    method: "post",
    data: data
  });
}

export function deleteTopics(id) {
  return request({
    url: `/dms/topics/${id}/`,
    method: "delete",
  });
}

export function editTopics(id, data) {
  return request({
    url: `/dms/topics/${id}/`,
    method: "patch",
    data: data
  });
}

