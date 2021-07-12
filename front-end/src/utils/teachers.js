export const TEACHER_POSTS = {
  CH: "Начальник ВУЦ",
  FH: "Начальник цикла",
  TE: "Профессорско-преподавательский состав",
};

export function displayTeacherMilgroups(milgroups) {
  return milgroups.map(m => m.title).join(", ");
}
