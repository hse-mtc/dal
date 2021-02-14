import request from "@/utils/request";
import { BASE_API_URL, DMS_URLS } from "@/constants/api";

export function nir(params) {
  return request({
    url: BASE_API_URL + DMS_URLS.nir.nir,
    method: "get",
    params,
  });
}
