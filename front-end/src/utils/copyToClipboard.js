const fallbackCopyTextToClipboard = text => {
  const textArea = document.createElement("textarea");

  textArea.value = text;
  textArea.style = "visible: none;top: 0;bottom: 0;position: fixed;max-width: 0;max-height: 0;";

  document.body.appendChild(textArea);

  textArea.focus();
  textArea.select();

  const isSuccess = (() => {
    try {
      return document.execCommand("copy");
    } catch (err) {
      console.error("fallback: Не удалось скопировать в буфер", err);
      this.$message.error("Не удалось скопировать в буфер");
      return false;
    }
  })();

  document.body.removeChild(textArea);

  return isSuccess;
};

/**
 * Копирует текст в буфер обмена и возвращает произошло ли это успешно
 *
 * @async
 * @param { String } text - текст, который нужно поместить в буфер
 * @returns { Promise<Boolean> } прошло ли копирование успешно
 */
const copyToClipboard = async text => {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch (e) {
    console.error("clipboard: Could not copy text: ", e);
    this.$message.error("Не удалось скопировать в буфер");
    return fallbackCopyTextToClipboard(text);
  }
};

export default copyToClipboard;
