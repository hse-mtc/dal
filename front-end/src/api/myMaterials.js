import request from "@/utils/request";

export function getMySubjects(id) {
    return request({
        url: `/dms/subjects/`,
        method: "get",
        params: {user: id}
    });
}
