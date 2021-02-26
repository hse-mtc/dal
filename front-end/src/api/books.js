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
export function editBook(id, data) {
  return request({
    url: `/dms/books/${id}/`,
    method: "PATCH",
    data,
  });
}

export function getFavoriteBooks(params) {
  return request({
    url: "/dms/favorite-books/",
    method: "get",
    params,
  });
}

export function saveFavBook(data) {
  return request({
    url: "/dms/favorite-books/",
    method: "post",
    data,
  });
}


export function unsaveFavBook(id) {
  return request({
    url: `/dms/favorite-books/${id}/`,
    method: "delete",
  });
}
