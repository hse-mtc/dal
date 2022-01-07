type Choice = {
  value: string,
  label: string,
}

type Choices = {
  // FIXME(TmLev): To be precise, returned type should be Choice or undefined.
  [key: string]: Choice;
}

export type { Choice, Choices };
