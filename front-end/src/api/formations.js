import request from "@/utils/request";
import { BASE_API_URL, LMS_URLS } from "@/constants/api";

const { reports, remarks, categories } = LMS_URLS.formations;

export const getFormationReports = params => request({
  url: BASE_API_URL + reports,
  method: "get",
  params,
});

export const getFormationRosterCount = milgroup => request({
  url: `${BASE_API_URL}${reports}roster-count/`,
  method: "get",
  params: { milgroup },
});

export const createFormationReport = data => request({
  url: BASE_API_URL + reports,
  method: "post",
  data,
});

export const updateFormationReport = (id, data) => request({
  url: `${BASE_API_URL}${reports}${id}/`,
  method: "patch",
  data,
});

export const getFormationCategories = () => request({
  url: BASE_API_URL + categories,
  method: "get",
});

export const createFormationRemark = data => request({
  url: BASE_API_URL + remarks,
  method: "post",
  data,
});

export const deleteFormationRemark = id => request({
  url: `${BASE_API_URL}${remarks}${id}/`,
  method: "delete",
});
