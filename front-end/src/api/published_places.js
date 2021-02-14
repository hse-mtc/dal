import request from "@/utils/request";
import { BASE_API_URL, DMS_URLS } from "@/constants/api";

export function getPublishPlaces(params) {
  return request({
    url: BASE_API_URL + DMS_URLS.publishers.publishers,
    method: "get",
    params,
  });
}
