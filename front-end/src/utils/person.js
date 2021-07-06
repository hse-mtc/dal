export function surnameWithInitials({ surname, name, patronymic }) {
  const nonEmptyWords = [surname, name, patronymic].filter(Boolean);
  const abbreviated = nonEmptyWords.map((word, index) => (index === 0 ? word : `${word[0]}.`));
  return abbreviated.join(" ");
}
