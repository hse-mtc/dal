import request from "@/utils/request";

export function getMilgroups(params) {
  return request({
    url: "/lms/milgroups",
    method: "get",
    params,
  });
}

export function getRanks(params) {
  return request({
    url: "/lms/ranks",
    method: "get",
    params,
  });
}

export function getPosts(params) {
  return request({
    url: "/lms/posts",
    method: "get",
    params,
  });
}

export function getSkills(params) {
  return request({
    url: "/lms/skills",
    method: "get",
    params,
  });
}
