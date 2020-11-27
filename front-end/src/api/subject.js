import request from "@/utils/request";

export function getSubject(params) {
  return request({
    url: `/dms/subjects/${params.id}/`,
    method: "get",
  });
}

export function deleteSubject(id) {
  return request({
    url: `/dms/subjects/${id}/`,
    method: "delete",
  });
}

export function upsertSubject(data) {
  if (data.id) {
    return request({
      url: `/dms/subjects/${data.id}/`,
      method: "patch",
      data: data,
    });
  } else {
    delete data.id;
    return request({
      url: `/dms/subjects/`,
      method: "post",
      data: data,
    });
  }
}

export function editSectionTitle(id, data) {
  return request({
    url: `/dms/sections/${id}/`,
    method: "patch",
    data: data,
  });
}

export function addSection(data) {
  return request({
    url: `/dms/sections/`,
    method: "post",
    data: data,
  });
}

export function deleteSection(id) {
  return request({
    url: `/dms/sections/${id}/`,
    method: "delete",
  });
}

export function addTopicFile(data) {
  return request({
    url: `/dms/class-materials/`,
    method: "post",
    data: data
  });
}
