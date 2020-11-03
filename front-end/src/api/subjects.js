import request from "@/utils/request";

export function getSubjects(params) {
  return request({
    url: "/dms/subjects/",
    method: "get",
    params,
  });
}
