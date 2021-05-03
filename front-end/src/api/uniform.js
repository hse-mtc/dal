import request from "@/utils/request";
import { LMS_URLS, BASE_API_URL } from "@/constants/api";

const {
  uniforms: { uniforms },
} = LMS_URLS;

export function getUniforms(params) {
  return request({
    url: BASE_API_URL + uniforms,
    method: "get",
    params,
  });
}

export function createUniform(data) {
  return request({
    url: BASE_API_URL + uniforms,
    method: "post",
    data,
  });
}

export function changeUniform(data, id) {
  return request({
    url: `${BASE_API_URL + uniforms}${id}/`,
    method: "patch",
    data,
  });
}
