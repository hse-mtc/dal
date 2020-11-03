/**
 * @param {string} path
 * @returns {Boolean}
 */
export function isExternal(path) {
  return /^(https?:|mailto:|tel:)/.test(path);
}

/**
 * @param {string} str
 * @returns {Boolean}
 */
export function validUsername(str) {
  let usernameRegex = /^[a-zA-Z0-9]+$/;
  const validUsername = str.trim().match(usernameRegex);
  if (validUsername == null) {
    alert("Неправильно введен логин");
    return false;
  }
  return true;
  // const valid_map = ['admin', 'editor', 'sampleuser', "vspelyak", "ivretjunskih"]
  // return valid_map.indexOf(str.trim()) >= 0
}
