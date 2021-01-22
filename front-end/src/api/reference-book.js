import request from "@/utils/request";

export function getReferenceBooks(params) {
  return request({
    url: "/lms/reference-book",
    method: "get",
    params,
  });
}
