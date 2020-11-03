import request from "@/utils/request";

export function getPaperCategories(params) {
  return request({
    url: "/dms/categories/",
    method: "get",
    params,
  });
}

export function addPaperCategories(data) {
  return request({
    url: "/dms/categories/",
    method: "post",
    data,
  });
}

export function deletePaperCategory(id) {
  return request({
    url: `/dms/categories/${id}/`,
    method: "delete",
  });
}
