export const BASE_API_URL = "api/";

export const AUTH_URLS = {
  refresh: "auth/tokens/refresh/",
  obtain: "auth/tokens/obtain/",
  user: "auth/user/",
  change_password: "auth/password/change/",
  permissions: "auth/permissions",
};

export const LMS_URLS = {
  register: {
    students: "lms/students/",
    teachers: "lms/teachers/",
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
  reference: {
    book: "lms/reference-book/",
    milgroups: "lms/milgroups/",
    ranks: "lms/ranks/",
    posts: "lms/teacher-posts/",
    milfaculties: "lms/milfaculties/",
    milspecialties: "lms/milspecialties/",
  },
  stuff: {
    student: "lms/students/",
    teacher: "lms/teachers/",
  },
  students: {
    students: "lms/students/",
    approvements: "lms/students/approvements/",
  },
  users: {
    users: "lms/users/",
    permissions: "lms/users/permissions",
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
