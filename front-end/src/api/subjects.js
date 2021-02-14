import request from "@/utils/request";
import { BASE_API_URL, DMS_URLS } from "@/constants/api";

const {subjects: {
  subjects,
  sections
}} = DMS_URLS

export function getSubjects(params) {
  return request({
    url: BASE_API_URL + subjects,
    method: "get",
    params,
  });
}

export function getSubject(params) {
  return request({
    url: `${BASE_API_URL}${subjects}${params.id}/`,
    method: "get",
  });
}

export function deleteSubject(id) {
  return request({
    url: `${BASE_API_URL}${subjects}${id}/`,
    method: "delete",
  });
}

export function upsertSubject(data) {
  if (data.id) {
    return request({
      url: `${BASE_API_URL}${subjects}${data.id}/`,
      method: "patch",
      data: data,
    });
  } else {
    delete data.id;
    return request({
      url: BASE_API_URL + subjects,
      method: "post",
      data: data,
    });
  }
}

export function editSectionTitle(id, data) {
  return request({
    url: `${BASE_API_URL}${sections}${id}/`,
    method: "patch",
    data: data,
  });
}

export function changeSectionOrder(id, order) {
  return request({
    url: `${BASE_API_URL}${sections}${id}/order/`,
    method: "patch",
    data: {
      to: order,
    },
  });
}

export function addSection(data) {
  return request({
    url: BASE_API_URL + sections,
    method: "post",
    data: data,
  });
}

export function deleteSection(id) {
  return request({
    url: `${BASE_API_URL}${sections}${id}/`,
    method: "delete",
  });
}
