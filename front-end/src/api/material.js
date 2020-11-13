import request from "@/utils/request";

export function deleteMaterial(id) {
  return request({
    url: `/dms/class-materials/${id}/`,
    method: "delete",
  });
}
