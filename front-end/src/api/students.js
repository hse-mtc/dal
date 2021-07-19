import request from "@/utils/request";
import { BASE_API_URL, LMS_URLS } from "@/constants/api";

const {
  staff: { students, applications, applicationsExport },
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
export function getStudentBasic(params) {
  return request({
    url: `${BASE_API_URL}${students}basic/`,
    method: "get",
    params,
  });
}

export function findStudentBasic(id) {
  return request({
    url: `${BASE_API_URL}${students}basic/${id}`,
    method: "get",
  });
}

export function findStudent(id) {
  return request({
    url: `${BASE_API_URL}${students}${id}/`,
    method: "get",
  });
}

export function findStudentSkills(id) {
  return request({
    url: `${BASE_API_URL}${students}skills/${id}/`,
    method: "get",
  });
}

export function findStudentPerformance(id) {
  return request({
    url: `${BASE_API_URL}${students}${id}/performance`,
    method: "get",
  });
}

export function findStudentExtra(id) {
  return request({
    url: `${BASE_API_URL}${students}extra/${id}/`,
    method: "get",
  });
}

export function postStudent(data) {
  return request({
    url: BASE_API_URL + students,
    method: "post",
    data: {
      ...data,
      generate_documents: __PROD__,
    },
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
