import request from "@/utils/request";
import { BASE_API_URL, LMS_URLS } from "@/constants/api";

const { choices } = LMS_URLS;

export function fetchAbsenceExcuses() {
  return request({
    url: BASE_API_URL + choices.absenceExcuses,
    method: "get",
  });
}

export function fetchAbsenceStatuses() {
  return request({
    url: BASE_API_URL + choices.absenceStatuses,
    method: "get",
  });
}

export function fetchEncouragementTypes() {
  return request({
    url: BASE_API_URL + choices.encouragementTypes,
    method: "get",
  });
}

export function fetchLessonTypes() {
  return request({
    url: BASE_API_URL + choices.lessonTypes,
    method: "get",
  });
}

export function fetchPunishmentTypes() {
  return request({
    url: BASE_API_URL + choices.punishmentTypes,
    method: "get",
  });
}

export function fetchStudentPosts() {
  return request({
    url: BASE_API_URL + choices.studentPosts,
    method: "get",
  });
}

export function fetchStudentStatuses() {
  return request({
    url: BASE_API_URL + choices.studentStatuses,
    method: "get",
  });
}

export function fetchTeacherPosts() {
  return request({
    url: BASE_API_URL + choices.teacherPosts,
    method: "get",
  });
}

export function fetchTeacherRanks() {
  return request({
    url: BASE_API_URL + choices.teacherRanks,
    method: "get",
  });
}
