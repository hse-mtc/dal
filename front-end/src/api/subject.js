import request from "@/utils/request";

export function getSubject(params) {
  return request({
    url: `/dms/subjects/${params.id}/`,
    method: "get",
  });
}
