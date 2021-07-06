import { Message } from "element-ui";

/**
 *
 * @param {Function} requestFunc - функция изменения, возвращает bool
 * @param {String} successMsg - сообщение успеха
 * @param {String} errorMsg - сообщение ошибки
 */
export const mutateData = async(requestFunc, successMsg, errorMsg) => {
  if (await requestFunc()) {
    Message({
      type: "success",
      message: successMsg,
    });
  } else {
    Message({
      type: "error",
      message: errorMsg,
    });
  }
};
