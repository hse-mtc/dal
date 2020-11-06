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
      data: data
    });
  } else {
    delete data.id
    return request({
      url: `/dms/subjects/`,
      method: "post",
      data: data
    });
  }
}
