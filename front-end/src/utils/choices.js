export const defaultChoiceLabelFromValue = (
  choices,
  value,
) => {
  const filtered = Object
    .values(choices)
    .filter(choice => choice.value === value);

  // If no exact match, return original value for debugging purposes.
  if (filtered.length !== 1) {
    return value;
  }

  return filtered[0].label;
};
