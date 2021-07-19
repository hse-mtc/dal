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

export const LMS_URLS = {
  register: {
    students: "lms/students/registration/",
    teachers: "lms/teachers/registration/",
  },
  absence: {
    absence: "lms/absences/",
    journal: "lms/absence-journal/",
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
    approvements: "lms/students/approvals/",
    applications: "lms/students/applications/",
    applicationsExport: "lms/students/applications/export/",
    notes: "lms/students/notes/",
  },
  users: {
    users: "lms/personnel-users",
  },
  uniforms: {
    uniforms: "lms/uniforms/",
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
