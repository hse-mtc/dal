import request from "@/utils/request";
import { BASE_API_URL, DMS_URLS } from "@/constants/api";

const {
  categories: { categories },
} = DMS_URLS;

export function getPaperCategories() {
  return request({
    url: BASE_API_URL + categories,
    method: "get",
  });
}

export function editPaperCategory(id, data) {
  return request({
    url: `${BASE_API_URL}${categories}${id}/`,
    method: "PATCH",
    data,
  });
}

export function addPaperCategory(data) {
  return request({
    url: BASE_API_URL + categories,
    method: "post",
    data,
  });
}

export function deletePaperCategory(id) {
  return request({
    url: `${BASE_API_URL}${categories}${id}/`,
    method: "delete",
  });
}
