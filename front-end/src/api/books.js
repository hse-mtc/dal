import request from "@/utils/request";

export function getBooks(params) {
  return request({
    url: "/dms/books/",
    method: "get",
    params,
  });
}

export function getBook(id) {
  return request({
    url: `/dms/books/${id}`,
    method: "get",
  });
}

export function uploadBook(data) {
  return request({
    url: "/dms/books/",
    method: "POST",
    data,
  });
}
