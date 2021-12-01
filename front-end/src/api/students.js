import request from "@/utils/request";
import { BASE_API_URL, AMS_URLS, LMS_URLS } from "@/constants/api";

const {
  staff: {
    students, notes,
  },
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

export function findStudentNotes(id) {
  return request({
    url: `${BASE_API_URL}${notes}`,
    method: "get",
    params: {
      student: id,
    },
  });
}

export function patchStudentNote(data) {
  return request({
    url: `${BASE_API_URL}${notes}${data.id}/`,
    method: "patch",
    data,
  });
}

export function postStudentNote(data) {
  return request({
    url: `${BASE_API_URL}${notes}`,
    method: "post",
    data,
  });
}

export function deleteStudentNote(id) {
  return request({
    url: `${BASE_API_URL}${notes}${id}`,
    method: "delete",
  });
}
