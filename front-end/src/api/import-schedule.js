import request from "@/utils/request";
import { LMS_URLS, BASE_API_URL } from "@/constants/api";

const {
  importSchedule: { parseSchedule, saveParsed },
} = LMS_URLS;

// eslint-disable-next-line
export function parseSchedulePost(data) {
  // todo
  // eslint-disable-next-line no-param-reassign
  return request({
    url: BASE_API_URL + parseSchedule,
    method: "post",
    data,
  });
}

// eslint-disable-next-line
export function saveParsedPost(data) {
  // todo
  // eslint-disable-next-line no-param-reassign
  return request({
    url: BASE_API_URL + saveParsed,
    method: "post",
    data,
  });
}
