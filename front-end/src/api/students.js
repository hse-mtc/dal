import request from "@/utils/request";
import { BASE_API_URL, LMS_URLS } from "@/constants/api";

const {
  stuff: { students, applications, applicationsExport },
} = LMS_URLS;

export const getStudents = filters => request({
  url: BASE_API_URL + students,
  method: "GET",
  data: filters,
});

export function getStudent(params) {
  return request({
    url: BASE_API_URL + students,
    method: "get",
    params,
  });
}

export function postStudent(data) {
  return request({
    url: BASE_API_URL + students,
    method: "post",
    data,
  });
}

export function patchStudent(data) {
  return request({
    url: `${BASE_API_URL}${students}${data.id}/`,
    method: "patch",
    data,
  });
}

export function deleteStudent(id) {
  return request({
    url: `${BASE_API_URL}${students}${id}/`,
    method: "delete",
  });
}

export const getApplicationsStudents = (page, pageSize, filters) => request({
  url: BASE_API_URL + applications,
  method: "GET",
  params: {
    page,
    page_size: pageSize,
    ...(filters || {}),
  },
});

export const updateStudentApplicationInfo = (id, data) => request({
  url: `${BASE_API_URL}${students}${id}/application/`,
  method: "PATCH",
  data,
});

export function getApplicationsExcelDownloadLink(campus) {
  return `${BASE_API_URL}${applicationsExport}?campus=${campus}`;
}
