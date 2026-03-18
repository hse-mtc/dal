import { AMS_URLS, BASE_API_URL } from "@/constants/api";
import request from "@/utils/request";

const {
  applicants: {
    applicants,
    register,
    applications,
    applicationsExport,
    applicationsCSPExport,
    applicationsDETExport,
    applicationsSTUDExport,
    exercises,
    exerciseResults,
  },
} = AMS_URLS;

export function postApplicant(data) {
  return request({
    url: BASE_API_URL + applicants,
    method: "post",
    data: {
      ...data,
      generate_documents: __PROD__,
    },
  });
}

export function putApplicant(id, data) {
  return request({
    url: `${BASE_API_URL}${applicants}${id}/`,
    method: "put",
    data: {
      ...data,
      generate_documents: __PROD__,
    },
  });
}

export function postEmail(data) {
  return request({
    url: BASE_API_URL + register,
    method: "post",
    data,
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
  url: `${BASE_API_URL}${applicants}${id}/application/`,
  method: "PATCH",
  data,
});

export const findApplicant = id => request({
  url: `${BASE_API_URL}${applicants}${id}/`,
  method: "GET",
});

export function resumbmitApplicantDocs() {
  return request({
    url: `${BASE_API_URL}${applicants}resubmit-docs/`,
    method: "POST",
  });
}

export const APPLICATIONS_EXPORT_LINK = `${BASE_API_URL}${applicationsExport}`;
export const APPLICATIONS_CSP_EXPORT_LINK = `${BASE_API_URL}${applicationsCSPExport}`;
export const APPLICATIONS_DET_EXPORT_LINK = `${BASE_API_URL}${applicationsDETExport}`;
export const APPLICATIONS_STUD_EXPORT_LINK = `${BASE_API_URL}${applicationsSTUDExport}`;

// GET /ams/physical/exercises/
export const getExercises = () => request({
  url: BASE_API_URL + exercises,
  method: "GET",
});

// GET /ams/applicants/{id}/exercise-results/
export const getExerciseResults = applicantId => request({
  url: `${BASE_API_URL}${exerciseResults}${applicantId}/exercise-results/`,
  method: "GET",
});

// POST /ams/applicants/{id}/exercise-results/
export const createExerciseResult = (applicantId, data) => request({
  url: `${BASE_API_URL}${exerciseResults}${applicantId}/exercise-results/`,
  method: "POST",
  data,
});

// PATCH /ams/applicants/{id}/exercise-results/{exerciseType}/
export const updateExerciseResult = (applicantId, exerciseType, data) => request({
  url: `${BASE_API_URL}${exerciseResults}${applicantId}/exercise-results/${exerciseType}/`,
  method: "PATCH",
  data,
});

// DELETE /ams/applicants/{id}/exercise-results/{exerciseType}/
export const deleteExerciseResult = (applicantId, exerciseType) => request({
  url: `${BASE_API_URL}${exerciseResults}${applicantId}/exercise-results/${exerciseType}/`,
  method: "DELETE",
});
