import { BASE_API_URL, DMS_URLS } from "@/constants/api";
import request from "@/utils/request";

export function getStatistics(id) {
  return request({
    url: `${BASE_API_URL}${DMS_URLS.statistics.statistics}${id}`,
    method: "get",
  });
}
