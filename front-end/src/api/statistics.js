import request from "@/utils/request";

export function getStatistics(id) {
  return request({
    url: `/dms/statistics/${id}`,
    method: "get",
  });
}
