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
    ranks,
    rooms,
    recruitmentOffices,
    skills,
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

export function getMilSpecialtiesSelectableByProgram(campus, program) {
  return request({
    url: BASE_API_URL + milspecialties,
    method: "get",
    params: { campus, program },
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

export function getProgramsByCampus(campus) {
  return request({
    url: BASE_API_URL + programs,
    method: "get",
    params: { campus },
  });
}

export function getAvailableForApplicantsProgramsByCampus(campus) {
  return request({
    url: BASE_API_URL + programs,
    method: "get",
    params: { campus, available_to_choose_for_applicants: true },
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
    url: BASE_API_URL + rooms,
    method: "get",
  });
}

export function editRoom(id, data) {
  return request({
    url: `${BASE_API_URL}${rooms}${id}/`,
    method: "PATCH",
    data,
  });
}

export function deleteRoom(id) {
  return request({
    url: `${BASE_API_URL}${rooms}${id}/`,
    method: "DELETE",
  });
}

export function addRoom(data) {
  return request({
    url: `${BASE_API_URL}${rooms}`,
    method: "POST",
    data,
  });
}

export function getSkills() {
  return request({
    url: BASE_API_URL + skills,
    method: "get",
  });
}

export function editSkill(id, data) {
  return request({
    url: `${BASE_API_URL}${skills}${id}/`,
    method: "PATCH",
    data,
  });
}

export function deleteSkill(id) {
  return request({
    url: `${BASE_API_URL}${skills}${id}/`,
    method: "DELETE",
  });
}

export function addSkill(data) {
  return request({
    url: `${BASE_API_URL}${skills}`,
    method: "POST",
    data,
  });
}

export function getRecruitmentOffices() {
  return request({
    url: `${BASE_API_URL}${recruitmentOffices}`,
    method: "GET",
  });
}
