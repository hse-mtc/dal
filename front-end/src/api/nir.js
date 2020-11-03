import request from "@/utils/request";

export function nir(params) {
  return request({
    url: "/dms/nir/",
    method: "get",
    params,
  });
}
