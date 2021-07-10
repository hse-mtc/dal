const { Message } = require("element-ui");

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
) => async function fetchRequest(newItem) {
  try {
    const { data } = await fetchFunc(newItem);

    mutation(data);

    return true;
  } catch (e) {
    console.error(`Не удалось загрузить ${errorMsg}:`, e);
    Message({
      type: "error",
      message: `Не удалось загрузить ${errorMsg}`,
    });

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
    Message({
      type: "error",
      message: `Не удалось добавить ${errorMsg}`,
    });

    return false;
  }
};

/**
 *
 * @param {unction} deleteFunc - функция удаления элемента
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
    Message({
      type: "error",
      message: `Не удалось удалить ${errorMsg}`,
    });

    return false;
  }
};

/**
 *
 * @param {unction} editFunc - функция изменения элемента
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
    Message({
      type: "error",
      message: `Не удалось изменить ${errorMsg}`,
    });

    return false;
  }
};
