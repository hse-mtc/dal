export function displayTeacherMilgroups(milgroups) {
  return milgroups.map(m => m.title).join(", ");
}
