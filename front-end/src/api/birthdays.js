import request from "@/utils/request";
import { BASE_API_URL, LMS_URLS } from "@/constants/api";

const {
  birthdays: { students, teachers },
} = LMS_URLS;

export function getStudentBirthdays(params) {
  return request({
    url: BASE_API_URL + students,
    method: "get",
    params,
  });
}

export function getTeacherBirthdays(params) {
  return request({
    url: BASE_API_URL + teachers,
    method: "get",
    params,
  });
}
