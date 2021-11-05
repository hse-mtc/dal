import CA from "@/assets/uniform-picker/cap.svg";
import HA from "@/assets/uniform-picker/hat.svg";

import PC from "@/assets/uniform-picker/pea-coat.svg";

export const TEACHER_POSTS = {
  CH: "Начальник ВУЦ",
  FH: "Начальник цикла",
  TE: "Профессорско-преподавательский состав",
};

export const CAMPUSES = {
  MO: "Москва",
  SP: "Санкт-Петербург",
  NN: "Нижний Новгород",
  PE: "Пермь",
};

export const APPLICATIONS_EXPORT_OPTIONS = {
  DEF: "по умолч.",
  CSP: "протокол",
};

export const STUDENT_POSTS = {
  GC: "Командир взвода",
  SC: "Командир отделения",
};

export const WEEKDAYS = [
  "Понедельник",
  "Вторник",
  "Среда",
  "Четверг",
  "Пятница",
  "Суббота",
  "Воскресенье",
];

export const EXCUSES = {
  LE: "Уважительная",
  IL: "Неуважительная",
  LA: "Опоздание",
};

export const ABSENCE_STATUSES = {
  OP: "Открыт",
  CL: "Закрыт",
};

export const ENCOURAGEMENT_TYPES = {
  EN: "Благодарность",
  RE: "Снятие взыскания",
};

export const PUNISHMENT_TYPES = {
  PU: "Взыскание",
  RE: "Выговор",
};

export const LESSON_TYPES = {
  SE: "Семинар",
  LE: "Лекция",
  GR: "Групповое занятия",
  PR: "Практическое занятие",
  FI: "Зачет",
  EX: "Экзамен",
};
export const HEADDRESSES = {
  CA, HA,
};
export const OUTERWEARS = {
  JA: "", // Uniform uses JA as default, so no picture is needed here.
  PC,
};
