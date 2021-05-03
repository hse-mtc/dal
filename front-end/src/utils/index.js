/**
 * Created by PanJiaChen on 16/11/18.
 */

/**
 * Parse the time to string
 * @param {(Object|string|number)} time
 * @param {string} cFormat
 * @returns {string | null}
 */
export function parseTime(rawTime, cFormat) {
  if (arguments.length === 0) {
    return null;
  }

  const format = cFormat || "{y}-{m}-{d} {h}:{i}:{s}";
  let date;
  let time;

  if (typeof rawTime === "object") {
    date = rawTime;
  } else {
    if (typeof time === "string" && /^[0-9]+$/.test(time)) {
      time = parseInt(rawTime, 10);
    }
    if (typeof time === "number" && time.toString().length === 10) {
      time = rawTime * 1000;
    }
    date = new Date(time);
  }

  const formatObj = {
    y: date.getFullYear(),
    m: date.getMonth() + 1,
    d: date.getDate(),
    h: date.getHours(),
    i: date.getMinutes(),
    s: date.getSeconds(),
    a: date.getDay(),
  };

  const timeStr = format.replace(/{([ymdhisa])+}/g, (result, key) => {
    const value = formatObj[key];
    // Note: getDay() returns 0 on Sunday
    if (key === "a") {
      return ["日", "一", "二", "三", "四", "五", "六"][value];
    }
    return value.toString().padStart(2, "0");
  });

  return timeStr;
}

/**
 * @param {number} time
 * @param {string} option
 * @returns {string}
 */
export function formatTime(rawTime, option) {
  let time;

  if ((`${rawTime}`).length === 10) {
    time = parseInt(time, 10) * 1000;
  } else {
    time = +time;
  }
  const d = new Date(time);
  const now = Date.now();

  const diff = (now - d) / 1000;

  if (diff < 30) {
    return "刚刚";
  } if (diff < 3600) {
    // less 1 hour
    return `${Math.ceil(diff / 60)}分钟前`;
  } if (diff < 3600 * 24) {
    return `${Math.ceil(diff / 3600)}小时前`;
  } if (diff < 3600 * 24 * 2) {
    return "1天前";
  }
  if (option) {
    return parseTime(time, option);
  }
  return (
    `${d.getMonth()
      + 1
    }月${
      d.getDate()
    }日${
      d.getHours()
    }时${
      d.getMinutes()
    }分`
  );
}

/**
 * @param {string} url
 * @returns {Object}
 */
export function param2Obj(url) {
  const search = url.split("?")[1];
  if (!search) {
    return {};
  }
  return JSON.parse(
    `{"${
      decodeURIComponent(search)
        .replace(/"/g, "\\\"")
        .replace(/&/g, "\",\"")
        .replace(/=/g, "\":\"")
        .replace(/\+/g, " ")
    }"}`,
  );
}
