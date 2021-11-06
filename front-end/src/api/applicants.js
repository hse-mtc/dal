import request from "@/utils/request";
import { AMS_URLS, BASE_API_URL } from "@/constants/api";

const {
  applicants: {
    applicants,
    applications,
    applicationsExport,
    applicationsCSPExport,
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

export const APPLICATIONS_EXPORT_LINK = `${BASE_API_URL}${applicationsExport}`;
export const APPLICATIONS_CSP_EXPORT_LINK = `${BASE_API_URL}${applicationsCSPExport}`;
