import request from "@/utils/request";
import { BASE_API_URL, DMS_URLS } from "@/constants/api";

const {papers: {papers}} = DMS_URLS

export function getPapers(
  category,
  authors,
  published_places,
  start_date,
  end_date,
  text,
  limit,
  offset
) {
  return request({
    url: BASE_API_URL + papers,
    method: "get",
    params: {
      category: category,
      authors: authors,
      publishers: published_places,
      start_date: start_date,
      end_date: end_date,
      search: text,
      limit: limit,
      offset: offset,
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
