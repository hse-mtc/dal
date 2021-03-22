import request from "@/utils/request";
import { BASE_API_URL, LMS_URLS } from "@/constants/api";

const {
  students: { students },
} = LMS_URLS;

export const addStudent = (data) =>
  request({
    url: BASE_API_URL + students,
    method: "post",
    data,
  });
