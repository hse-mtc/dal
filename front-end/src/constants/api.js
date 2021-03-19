export const BASE_API_URL = 'api/'

export const AUTH_URLS = {
  refresh: 'auth/tokens/refresh/',
  obtain: 'auth/tokens/obtain/',
  profile: 'auth/profile/',
  change_password: 'auth/password/change/',
}

export const LMS_URLS = {
  register: {
    students: 'lms/students/',
    teachers: 'lms/teachers/'
  },
  absence: {
    absence: 'lms/absence/',
    journal: 'lms/absence-journal/'
  },
  encouragement: {
    encouragement: 'lms/encouragement/'
  },
  lessons: {
    lesson: 'lms/lesson/',
    journal: 'lms/lesson-journal/'
  },
  marks: {
    mark: 'lms/mark/',
    journal: 'lms/mark-journal/',
  },
  punishment: {
    punishment: 'lms/punishment/'
  },
  reference: {
    book: 'lms/reference-book/',
    milgroups: 'lms/milgroups/',
    ranks: 'lms/ranks/',
    posts: 'lms/teacher-posts/',
    milfaculties: 'lms/milfaculties/',
  },
  stuff: {
    student: 'lms/student/',
    teacher: 'lms/teacher/'
  },
  students: {
    students: 'lms/students/'
  }
}

export const DMS_URLS = {
  authors: {
    authors: 'dms/authors/'
  },
  books: {
    books: 'dms/books/',
    favorite: 'dms/favorite-books/'

  },
  papers: {
    papers: 'dms/papers/'
  },
  materials: {
    class: 'dms/class-materials/'
  },
  tags: {
    tags: 'dms/tags/'
  },
  categories: {
    categories: 'dms/categories/'
  },
  publishers: {
    publishers: 'dms/publishers/'
  },
  subjects: {
    subjects: 'dms/subjects/',
    sections: 'dms/sections/',
    topics: 'dms/topics/'
  },
  statistics: {
    statistics: 'dms/statistics/'
  }
}
