import { Message } from "element-ui";

function details(status) {
  switch (status) {
    case 400:
      return "Неверный формат данных.";
    case 401:
      return "Необходима авторизация.";
    case 403:
      return "Доступ запрещен.";
    case 404:
      return "Данные не найдены.";
    case 500:
      return "Внутренняя ошибка сервера.";
    case 504:
      return "Сервер не отвечает.";
    default:
      return "Причина неизвестна.";
  }
}

export function getError(entity, status) {
  Message({
    message: `Ошибка при получении ${entity}. ${details(status)}`,
    type: "error",
  });
}

export function postError(entity, status) {
  Message({
    message: `Ошибка при создании ${entity}. ${details(status)}`,
    type: "error",
  });
}

export function patchError(entity, status) {
  Message({
    message: `Ошибка при редактировании ${entity}. ${details(status)}`,
    type: "error",
  });
}

export function deleteError(entity, status) {
  Message({
    message: `Ошибка при удалении ${entity}. ${details(status)}`,
    type: "error",
  });
}

export function orderError(entity, status) {
  Message({
    message: `Ошибка при перемещении ${entity}. ${details(status)}`,
    type: "error",
  });
}

export function postSuccess(entity) {
  Message({
    message: `Создание ${entity} прошло успешно.`,
    type: "success",
  });
}

export function patchSuccess(entity) {
  Message({
    message: `Редактирование ${entity} прошло успешно.`,
    type: "success",
  });
}

export function deleteSuccess(entity) {
  Message({
    message: `Удаление ${entity} прошло успешно.`,
    type: "success",
  });
}

export function downloadError(entity, status) {
  Message({
    message: `Ошибка при удалении ${entity}. ${details(status)}`,
    type: "error",
  });
}
