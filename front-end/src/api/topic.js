import request from "@/utils/request";
import { BASE_API_URL, DMS_URLS } from "@/constants/api";

const {
  subjects: { topics, sections },
} = DMS_URLS;

export function getTopics(id) {
  return request({
    url: `${BASE_API_URL}${sections}${id}/`,
    method: "get",
  });
}

export function addTopics(data) {
  return request({
    url: BASE_API_URL + topics,
    method: "post",
    data,
  });
}

export function deleteTopics(id) {
  return request({
    url: `${BASE_API_URL}${topics}${id}/`,
    method: "delete",
  });
}

export function editTopics(id, data) {
  return request({
    url: `${BASE_API_URL}${topics}${id}/`,
    method: "patch",
    data,
  });
}

export function changeTopicOrder(id, order) {
  return request({
    url: `${BASE_API_URL}${topics}${id}/order/`,
    method: "patch",
    data: {
      to: order,
    },
  });
}
