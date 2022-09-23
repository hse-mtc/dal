import request from "@/utils/request";
import { BASE_API_URL, DMS_URLS } from "@/constants/api";

const classMaterials = DMS_URLS.materials.class;

export function deleteMaterial(id) {
  return request({
    url: `${BASE_API_URL}${classMaterials}${id}/`,
    method: "delete",
  });
}

export function addTopicFile(data) {
  return request({
    url: BASE_API_URL + classMaterials,
    method: "post",
    data,
    timeout: 60000, 
  });
}
