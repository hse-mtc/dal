import request from "@/utils/request";

export function deleteDocument(id) {
  return request({
    url: `/dms/papers/${id}/`,
    method: "delete",
  });
}
