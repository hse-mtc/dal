import { Choices } from "@/types/choices";

export const defaultChoiceLabelFromValue = (
  choices: Choices,
  value: string,
  defaultLabel: string = value,
): string => {
  const filtered = Object
    .values(choices)
    .filter(choice => choice.value === value);

  // If no exact match happened, return `defaultLabel`.
  if (filtered.length !== 1) {
    return defaultLabel;
  }

  return filtered[0].label;
};
