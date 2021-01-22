import { Message } from "element-ui";

export function getError(entity) {
    Message({
        message: `Ошибка при получении ${entity}.`,
        type: 'error'
    })
}

export function postError(entity) {
    Message({
        message: `Ошибка при создании ${entity}.`,
        type: 'error'
    })
}

export function patchError(entity) {
    Message({
        message: `Ошибка при редактировании ${entity}.`,
        type: 'error'
    })
}

export function deleteError(entity) {
    Message({
        message: `Ошибка при удалении ${entity}.`,
        type: 'error'
    })
}

export function postSuccess(entity) {
    Message({
        message: `Создание ${entity} прошло успешно.`,
        type: 'success'
    })
}

export function patchSuccess(entity) {
    Message({
        message: `Редактирование ${entity} прошло успешно.`,
        type: 'success'
    })
}



export function deleteSuccess(entity) {
    Message({
        message: `Удаление ${entity} прошло успешноe.`,
        type: 'success'
    })
}
