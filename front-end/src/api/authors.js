import request from "@/utils/request";
import { BASE_API_URL, DMS_URLS } from "@/constants/api";

export function getAuthors(params) {
  return request({
    url: BASE_API_URL + DMS_URLS.authors.authors,
    method: "get",
    params,
  });
}
