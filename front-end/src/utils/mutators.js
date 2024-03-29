import {
  deleteError,
  getError,
  orderError,
  patchError,
  postError,
} from "@/utils/message";

/**
 *
 * @param {function} fetchFunc - функция запрашивающая данные
 * @param {function} mutation - принимает на вход результат fetchFunc
 * @param {string} errorMsg - что не удалось загрузить
 * @returns {function}
 */
export const getFetchRequest = (
  fetchFunc,
  mutation,
  errorMsg,
) => async function fetchRequest() {
  try {
    const { data } = await fetchFunc();

    mutation(data);

    return true;
  } catch (e) {
    console.error(`Не удалось загрузить ${errorMsg}:`, e);
    getError(errorMsg, e.response?.status);
    return false;
  }
};

/**
 *
 * @param {function} addFunc - функция добавления элемента
 * @param {function} mutation - принимает на вход обновленный массив
 * @param {string} mutationFiled - поле в котором хранятся данные
 * @param {string} errorMsg - что не удалось добавить
 * @returns {function}
 */
export const getAddRequest = (
  addFunc,
  mutation,
  mutationFiled,
  errorMsg,
) => async function addRequest(newItem) {
  try {
    const { data } = await addFunc(newItem);

    mutation([...this[mutationFiled], data]);

    return true;
  } catch (e) {
    console.error(`Не удалось добавить ${errorMsg}:`, e);
    postError(errorMsg, e.response?.status);
    return false;
  }
};

/**
 *
 * @param {function} deleteFunc - функция удаления элемента
 * @param {function} mutation - принимает на вход обновленный массив
 * @param {string} mutationFiled - поле в котором хранятся данные
 * @param {string} errorMsg - что не удалось удалить
 * @returns {function}
 */
export const getDeleteRequest = (
  deleteFunc,
  mutation,
  mutationFiled,
  errorMsg,
) => async function deleteRequest(id) {
  try {
    await deleteFunc(id);

    mutation(this[mutationFiled].filter(item => item.id !== id));
    return true;
  } catch (e) {
    console.error(`Не удалось удалить ${errorMsg}:`, e);
    deleteError(errorMsg, e.response?.status);
    return false;
  }
};

/**
 *
 * @param {function} editFunc - функция изменения элемента
 * @param {function} mutation - принимает на вход обновленный массив
 * @param {string} mutationFiled - поле в котором хранятся данные
 * @param {string} errorMsg - что не удалось изменить
 * @returns {function}
 */
export const getEditRequest = (
  editFunc,
  mutation,
  mutationFiled,
  errorMsg,
) => async function editRequest({ id, ...newData }) {
  try {
    const { data } = await editFunc(id, newData);

    const index = this[mutationFiled].findIndex(item => item.id === id);
    const newArray = [...this[mutationFiled]];
    newArray[index] = data;

    mutation(newArray);

    return true;
  } catch (e) {
    console.error(`Не удалось изменить ${errorMsg}:`, e);
    patchError(errorMsg, e.response?.status);
    return false;
  }
};

/**
 *
 * @param {function} orderFunc - функция перемещения элемента
 * @param {function} mutation - принимает на вход обновленный массив
 * @param {string} mutationFiled - поле в котором хранятся данные
 * @param {string} errorMsg - что не удалось переместить
 * @returns {function}
 */
export const getOrderChangeRequest = (
  orderFunc,
  mutation,
  mutationFiled,
  errorMsg,
) => async function orderRequest(id, order) {
  try {
    await orderFunc(id, order);

    const newOrder = [...this[mutationFiled]];
    const elementIndex = newOrder.findIndex(item => item.id === id);
    const temp = newOrder[elementIndex];

    newOrder.splice(elementIndex, 1);
    newOrder.splice(order, 0, temp);

    // eslint-disable-next-line no-param-reassign
    newOrder.forEach((item, index) => { item.order = index; });

    mutation(newOrder);
    return true;
  } catch (e) {
    console.error(`Не удалось переместить ${errorMsg}:`, e);
    orderError(errorMsg, e.response?.status);
    return false;
  }
};
