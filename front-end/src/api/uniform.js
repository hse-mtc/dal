import request from "@/utils/request";
import { LMS_URLS, BASE_API_URL } from "@/constants/api";

const {
  uniforms: { uniforms },
} = LMS_URLS;

export function getUniforms() {
  return request({
    url: BASE_API_URL + uniforms,
    method: "get",
  });
}

export function createUniform(params) {
  return request({
    url: BASE_API_URL + uniforms,
    method: "post",
    params,
  });
}

export function changeUniform(params, id) {
  return request({
    url: BASE_API_URL + uniforms + `${id}/`,
    method: "patch",
    params,
  });
}
