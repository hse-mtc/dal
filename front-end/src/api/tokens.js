import request from "@/utils/request";
import { AUTH_URLS, BASE_API_URL } from "@/constants/api";

export function updateAccess(data) {
  return request({
    url: BASE_API_URL + AUTH_URLS.refresh,
    method: "post",
    data,
  });
}
