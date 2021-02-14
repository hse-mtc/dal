import request from "@/utils/request";
import { BASE_API_URL, DMS_URLS } from "@/constants/api";

const {books: {books}} = DMS_URLS

export function getBooks(params) {
  return request({
    url: BASE_API_URL + books,
    method: "get",
    params,
  });
}

export function getBook(id) {
  return request({
    url: `${BASE_API_URL}${books}${id}`,
    method: "get",
  });
}

export function uploadBook(data) {
  return request({
    url: BASE_API_URL + books,
    method: "POST",
    data,
  });
}

export function editBook(id, data) {
  return request({
    url: `${BASE_API_URL}${books}${id}/`,
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
