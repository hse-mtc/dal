import request from "@/utils/request";
import { BASE_API_URL, DMS_URLS } from "@/constants/api";

export function getExistingTags(params) {
  return request({
    url: BASE_API_URL + DMS_URLS.tags.tags,
    method: "get",
    params,
  });
}
