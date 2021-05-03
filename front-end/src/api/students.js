import request from "@/utils/request";
import { BASE_API_URL, LMS_URLS } from "@/constants/api";

const {
  students: { students, applications },
} = LMS_URLS;

export const addStudent = data => request({
  url: BASE_API_URL + students,
  method: "post",
  data,
});

export const getStudents = filters => request({
  url: BASE_API_URL + students,
  method: "GET",
  data: filters,
});

export const getApplicationsStudents = (page, pageSize, filters) => request({
  url: BASE_API_URL + applications,
  method: "GET",
  params: {
    page,
    page_size: pageSize,
    ...(filters || {}),
  },
});
