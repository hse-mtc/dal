import { BASE_API_URL, LMS_URLS } from "@/constants/api";
import request from "@/utils/request";

const {
  recovery: { recovery },
} = LMS_URLS;

export function sendRecoveryEmail(data) {
  return request({
    url: BASE_API_URL + recovery,
    method: "post",
    data,
  });
}
