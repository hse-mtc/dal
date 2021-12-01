export const defaultChoiceLabelFromValue = (
  choices,
  value,
  defaultLabel = value,
) => {
  const filtered = Object
    .values(choices)
    .filter(choice => choice.value === value);

  // If no exact match happened, return `defaultLabel`.
  if (filtered.length !== 1) {
    return defaultLabel;
  }

  return filtered[0].label;
};
