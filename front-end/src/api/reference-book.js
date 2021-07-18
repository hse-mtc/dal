import request from "@/utils/request";
import { BASE_API_URL, LMS_URLS } from "@/constants/api";

const {
  reference: {
    book,
    milspecialties,
    milgroups,
    achievementTypes,
    milfaculties,
    programs,
  },
} = LMS_URLS;

export function getReferenceBooks(params) {
  return request({
    url: BASE_API_URL + book,
    method: "get",
    params,
  });
}

export function getMilSpecialties(campus) {
  return request({
    url: BASE_API_URL + milspecialties,
    method: "get",
    params: { campus },
  });
}

export function editMilSpecialty(id, data) {
  return request({
    url: `${BASE_API_URL}${milspecialties}${id}/`,
    method: "PATCH",
    data,
  });
}

export function deleteMilSpecialty(id) {
  return request({
    url: `${BASE_API_URL}${milspecialties}${id}/`,
    method: "DELETE",
  });
}

export function addMilSpecialty(data) {
  return request({
    url: `${BASE_API_URL}${milspecialties}`,
    method: "POST",
    data,
  });
}

export function getMilGroups() {
  return request({
    url: BASE_API_URL + milgroups,
    method: "get",
  });
}

export function editMilGroup(id, data) {
  return request({
    url: `${BASE_API_URL}${milgroups}${id}/`,
    method: "PATCH",
    data,
  });
}

export function deleteMilGroup(id) {
  return request({
    url: `${BASE_API_URL}${milgroups}${id}/`,
    method: "DELETE",
  });
}

export function addMilGroup(data) {
  return request({
    url: `${BASE_API_URL}${milgroups}`,
    method: "POST",
    data,
  });
}

export function getMilFaculties() {
  return request({
    url: BASE_API_URL + milfaculties,
    method: "get",
  });
}

export function editMilFaculty(id, data) {
  return request({
    url: `${BASE_API_URL}${milfaculties}${id}/`,
    method: "PATCH",
    data,
  });
}

export function deleteMilFaculty(id) {
  return request({
    url: `${BASE_API_URL}${milfaculties}${id}/`,
    method: "DELETE",
  });
}

export function addMilFaculty(data) {
  return request({
    url: `${BASE_API_URL}${milfaculties}`,
    method: "POST",
    data,
  });
}

export function getRanks() {
  return request({
    url: BASE_API_URL + LMS_URLS.reference.ranks,
    method: "get",
  });
}

export function getTeacherPosts() {
  return request({
    url: BASE_API_URL + LMS_URLS.reference.teacherPosts,
    method: "get",
  });
}

export function getStudentPosts() {
  return request({
    url: BASE_API_URL + LMS_URLS.reference.studentPosts,
    method: "get",
  });
}

export function getAchievementTypes() {
  return request({
    url: BASE_API_URL + achievementTypes,
    method: "get",
  });
}

export function editAchievementType(id, data) {
  return request({
    url: `${BASE_API_URL}${achievementTypes}${id}/`,
    method: "PATCH",
    data,
  });
}

export function deleteAchievementType(id) {
  return request({
    url: `${BASE_API_URL}${achievementTypes}${id}/`,
    method: "DELETE",
  });
}

export function addAchievementType(data) {
  return request({
    url: `${BASE_API_URL}${achievementTypes}`,
    method: "POST",
    data,
  });
}

export function getPrograms() {
  return request({
    url: BASE_API_URL + programs,
    method: "get",
  });
}

export function editProgram(id, data) {
  return request({
    url: `${BASE_API_URL}${programs}${id}/`,
    method: "PATCH",
    data,
  });
}

export function deleteProgram(id) {
  return request({
    url: `${BASE_API_URL}${programs}${id}/`,
    method: "DELETE",
  });
}

export function addProgram(data) {
  return request({
    url: `${BASE_API_URL}${programs}`,
    method: "POST",
    data,
  });
}

export function getRooms() {
  return request({
    url: BASE_API_URL + LMS_URLS.reference.rooms,
    method: "get",
  });
}

export function getSkills() {
  return request({
    url: BASE_API_URL + LMS_URLS.reference.skills,
    method: "get",
  });
}
