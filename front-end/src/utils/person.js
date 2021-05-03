export function surnameWithInitials({ surname, name, patronymic }) {
  const nonEmptyWords = [surname, name, patronymic].filter(w => w);
  const abbreviated = nonEmptyWords.map((word, index) => (index === 0 ? word : `${word[0]}.`));
  return abbreviated.join(" ");
}
