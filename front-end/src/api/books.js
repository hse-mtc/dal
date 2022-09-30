import request from "@/utils/request";
import { BASE_API_URL, DMS_URLS } from "@/constants/api";

const {
  books: { books, favorite },
} = DMS_URLS;

export function getBooks(params) {
  return request({
    url: BASE_API_URL + books,
    method: "get",
    params,
  });
}

export function getBook(id) {
  return request({
    url: `${BASE_API_URL}${books}${id}/`,
    method: "get",
  });
}

export function deleteBook(id) {
  return request({
    url: `${BASE_API_URL}${books}${id}/`,
    method: "delete",
  });
}

export function uploadBook(data) {
  console.log(data);
  return request({
    url: BASE_API_URL + books,
    method: "POST",
    data,
    timeout: 60000,
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
    url: BASE_API_URL + favorite,
    method: "get",
    params,
  });
}

export function saveFavBook(data) {
  console.log(data);
  return request({
    url: BASE_API_URL + favorite,
    method: "post",
    data,
  });
}

export function unsaveFavBook(id) {
  return request({
    url: `${BASE_API_URL}${favorite}${id}/`,
    method: "delete",
  });
}
