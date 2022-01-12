export const BASE_API_URL = "api/";

export const AUTH_URLS = {
  refresh: "auth/tokens/refresh/",
  obtain: "auth/tokens/obtain/",
  user: "auth/user/",
  change_password: "auth/password/change/",
  permissions: "auth/permissions/",
  userControl: "auth/user-control/",
  roles: "auth/group/",
};

export const AMS_URLS = {
  applicants: {
    applicants: "ams/applicants/",
    register: "ams/register/",
    applications: "ams/applicants/applications/",
    applicationsExport: "ams/applicants/applications/export/",
    applicationsCSPExport: "ams/applicants/applications/competitive-selection-protocol/export/",
  },
};

export const LMS_URLS = {
  register: {
    students: "lms/students/registration/",
    teachers: "lms/teachers/registration/",
  },
  absence: {
    absence: "lms/absences/",
    journal: "lms/absence-journal/",
    attachment: "lms/absence-attachments/",
  },
  encouragement: {
    encouragement: "lms/encouragements/",
  },
  lessons: {
    lesson: "lms/lessons/",
    journal: "lms/lesson-journal/",
  },
  marks: {
    mark: "lms/marks/",
    journal: "lms/mark-journal/",
  },
  punishment: {
    punishment: "lms/punishments/",
  },
  achievement: {
    achievement: "lms/achievements/",
  },
  subject: {
    subject: "lms/subjects/",
  },
  reference: {
    book: "lms/reference-book/",
    milgroups: "lms/milgroups/",
    ranks: "lms/ranks/",
    milfaculties: "lms/milfaculties/",
    milspecialties: "lms/milspecialties/",
    achievementTypes: "lms/achievement-types/",
    programs: "lms/programs/",
    rooms: "lms/rooms/",
    skills: "lms/skills/",
  },
  staff: {
    students: "lms/students/",
    teachers: "lms/teachers/",
    teachersApprovals: "lms/teachers/approvals/",
    notes: "lms/students/notes/",
  },
  users: {
    users: "lms/personnel-users",
  },
  uniforms: {
    uniforms: "lms/uniforms/",
  },
  birthdays: {
    students: "lms/birthdays/students",
    teachers: "lms/birthdays/teachers",
  },
  choices: {
    absenceExcuses: "lms/choices/absence-excuses/",
    absenceStatuses: "lms/choices/absence-statuses/",
    encouragementTypes: "lms/choices/encouragement-types/",
    lessonTypes: "lms/choices/lesson-types/",
    punishmentTypes: "lms/choices/punishment-types/",
    studentPosts: "lms/choices/student-posts/",
    studentStatuses: "lms/choices/student-statuses/",
    teacherPosts: "lms/choices/teacher-posts/",
    teacherRanks: "lms/choices/teacher-ranks/",
  },
};

export const DMS_URLS = {
  authors: {
    authors: "dms/authors/",
  },
  books: {
    books: "dms/books/",
    favorite: "dms/favorite-books/",
  },
  papers: {
    papers: "dms/papers/",
  },
  materials: {
    class: "dms/class-materials/",
  },
  tags: {
    tags: "dms/tags/",
  },
  categories: {
    categories: "dms/categories/",
  },
  publishers: {
    publishers: "dms/publishers/",
  },
  subjects: {
    subjects: "dms/subjects/",
    sections: "dms/sections/",
    topics: "dms/topics/",
  },
  statistics: {
    statistics: "dms/statistics/",
  },
};
