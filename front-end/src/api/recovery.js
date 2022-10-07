import { BASE_API_URL, AUTH_URLS } from "@/constants/api";
import request from "@/utils/request";

export function sendRecoveryEmail(data) {
  return request({
    url: BASE_API_URL + AUTH_URLS.recovery,
    method: "post",
    data,
  });
}
