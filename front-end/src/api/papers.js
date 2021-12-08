import request from "@/utils/request";
import { BASE_API_URL, DMS_URLS } from "@/constants/api";

const {
  papers: { papers },
} = DMS_URLS;

export function getPapers(page, pageSize, params) {
  return request({
    url: BASE_API_URL + papers,
    method: "get",
    params: {
      page,
      page_size: pageSize,
      params,
    },
  });
}

export function postPaper(data) {
  return request({
    url: BASE_API_URL + papers,
    method: "post",
    headers: {
      "Content-Type": "multipart/form-data",
    },
    data,
  });
}

export function patchPaper(id, data) {
  return request({
    url: `${BASE_API_URL}${papers}${id}/`,
    method: "patch",
    headers: {
      "Content-Type": "multipart/form-data",
    },
    data,
  });
}
