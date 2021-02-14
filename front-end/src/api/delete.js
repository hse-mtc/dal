import request from "@/utils/request";
import { BASE_API_URL, DMS_URLS } from "@/constants/api";

export function deleteDocument(id) {
  return request({
    url: `${BASE_API_URL}${DMS_URLS.papers.papers}${id}/`,
    method: "delete",
  });
}
