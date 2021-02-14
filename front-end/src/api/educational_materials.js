import request from "@/utils/request";
import { BASE_API_URL, DMS_URLS } from "@/constants/api";

export function getEducationalMaterials(params) {
  return request({
    url: BASE_API_URL + DMS_URLS.materials.educational,
    method: "get",
    params,
  });
}
