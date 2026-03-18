import request from "@/utils/request";
import { BASE_API_URL, DMS_URLS } from "@/constants/api";

const {
  videos: { videos },
} = DMS_URLS;

export function getVideos(params) {
  return request({
    url: BASE_API_URL + videos,
    method: "get",
    params,
  });
}

export function getVideo(id) {
  return request({
    url: `${BASE_API_URL}${videos}${id}/`,
    method: "get",
  });
}

export function uploadVideo(data) {
  return request({
    url: BASE_API_URL + videos,
    method: "post",
    data,
    timeout: 60000,
  });
}

export function editVideo(id, data) {
  return request({
    url: `${BASE_API_URL}${videos}${id}/`,
    method: "patch",
    data,
    timeout: 60000,
  });
}

export function deleteVideo(id) {
  return request({
    url: `${BASE_API_URL}${videos}${id}/`,
    method: "delete",
  });
}
