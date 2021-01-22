import request from "@/utils/request";

export function getBooks(params) {
  return request({
    url: "/dms/books/",
    method: "get",
    params,
  });
}
