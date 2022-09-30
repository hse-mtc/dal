import Vue from "vue";
import Router from "vue-router";

/* Layout */
import Layout from "@/layout";
import AppMain from "@/layout/components/AppMain";

Vue.use(Router);

/**
 * Note: sub-menu only appear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * displayInner                   if true move inner routes to root
 * redirect: noRedirect           if set noRedirect will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'             the icon show in the sidebar
    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
    activeMenu: '/example/list'  if set path, the sidebar will highlight the path you set
  }
 */

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const constantRoutes = [
  {
    name: "Login",
    path: "/login/",
    component: () => import("@/views/login/index"),
    hidden: true,
  },
  {
    name: "TeacherRegistration",
    path: "/teacher-registration/",
    component: () => import("@/views/TeacherRegistration/index"),
    hidden: true,
  },
  {
    name: "StudentRegistration",
    path: "/student-registration/",
    component: () => import("@/views/StudentsRegistration/index"),
    hidden: true,
  },
  {
    path: "/change-password/",
    component: () => import("@/views/ChangePassword/index"),
    hidden: true,
  },
  {
    path: "/recovery/",
    component: () => import("@/views/Recovery/index"),
    hidden: true,
  },

  {
    path: "/applicant-form/",
    name: "ApplicantForm",
    component: () => import("@/views/ApplicantForm/index.vue"),
    meta: { title: "Форма поступления" },
    hidden: true,
  },

  {
    path: "/applicant-registration/",
    name: "ApplicantRegistration",
    component: () => import("@/views/ApplicantRegistration/index.vue"),
    meta: { title: "Регистрация абитуриента" },
    hidden: true,
  },

  // FIXME(ShishckovA): doesn't work, have to change (i.e. pushing instead of patching), fix and test
  // {
  //   path: "/applicant-to-student/",
  //   name: "ApplicantToStudent",
  //   component: () => import("@/views/ApplicantToStudent/index.vue"),
  //   meta: { title: "Регистрация студента", icon: "journal", permissions: ["applicant.applicant.self"] },
  //   hidden: true,
  // },

  {
    path: "/",
    redirect: "/my-materials/",
    component: Layout,
    displayInner: true,
    children: [
      {
        path: "my-materials/",
        name: "Мои материалы",
        component: () => import("@/views/myMaterials/index"),
        meta: { title: "Мои материалы", icon: "materials" },
      },

      {
        path: "papers/",
        name: "Papers",
        component: () => import("@/views/Papers/index"),
        meta: { title: "Военно-научные работы", icon: "study", permissions: ["papers.get.all"] },
      },

      {
        path: "library/",
        name: "Library",
        component: () => import("@/views/Library/index"),
        meta: { title: "Электронная библиотека", icon: "books", permissions: ["books.get.all", "books.get.self"] },
      },

      {
        path: "library/book/:id/",
        name: "Book",
        component: () => import("@/views/Book/index"),
        meta: { title: "Электронная библиотека" },
        hidden: true,
      },

      {
        path: "discipline-control/",
        name: "DisciplineControl",
        meta: { title: "Учебные дисциплины", icon: "book" },
        component: AppMain,
        children: [
          {
            path: "subjects/",
            name: "Subjects",
            component: () => import("@/views/Subjects/index"),
            meta: { title: "Методические материалы", icon: "presentation", permissions: ["class-materials.get.all", "class-materials.get.self"] },
          },
          {
            path: "subjects/:subjectId/",
            hidden: true,
            name: "Subject",
            component: () => import("@/views/Subject/index"),
            meta: { title: "Учебно-методические материалы" },
          },
          {
            path: "schedule/",
            name: "Schedule",
            component: () => import("@/views/Schedule/index"),
            meta: { title: "Расписание занятий", icon: "calendar", permissions: ["lessons.get.all", "lessons.get.milfaculty", "lessons.get.milgroup"] },
          },
          {
            path: "marks/",
            name: "Marks",
            component: () => import("@/views/Marks/index"),
            meta: { title: "Журнал оценок", icon: "journal", permissions: ["marks.get.all", "marks.get.milfaculty", "marks.get.milgroup", "marks.get.self"] },
          },
        ],
      },

      {
        path: "personnel/",
        name: "Personnel",
        component: () => import("@/views/Personnel/index"),
        meta: { title: "Личный состав ВУЦ", icon: "people" },
      },

      {
        path: "student/:studentId",
        name: "Student",
        component: () => import("@/views/Personnel/Student"),
        meta: { title: "Студент" },
        hidden: true,
      },
      {
        path: "teacher/:teacherId",
        name: "Teacher",
        component: () => import("@/views/Personnel/Teacher"),
        meta: { title: "Преподаватель" },
        hidden: true,
      },

      {
        path: "absence/",
        name: "Absence",
        component: () => import("@/views/Absence/index"),
        meta: { title: "Журнал посещаемости", icon: "session-log", permissions: ["absences.get.all", "absences.get.milfaculty", "absences.get.milgroup", "absences.get.self"] },
      },

      {
        path: "discipline/",
        name: "Discipline",
        component: () => import("@/views/Discipline/index"),
        meta: {
          title: "Дисциплинарная практика",
          icon: "cross",
          permissions:
            [
              "encouragements.get.all", "encouragements.get.milfaculty", "encouragements.get.milgroup", "encouragements.get.self",
              "punishments.get.all", "punishments.get.milfaculty", "punishments.get.milgroup", "punishments.get.self",
            ],
        },
      },

      {
        path: "apanel/",
        name: "AdminPanel",
        component: () => import("@/views/AdminPanel/index"),
        meta: { title: "Панель администратора", icon: "journal", permissions: ["permissions.get.all", "subjects.get.all", "subjects.get.self"] },
        children: [
          {
            path: "approve-teachers/",
            name: "approve-teachers",
            component: () => import("@/components/Apanel/Approve/ApproveTeachers.vue"),
            meta: { title: "Подтверждения" },
            hidden: true,
          },
          {
            path: "approve-students/",
            name: "approve-students",
            component: () => import("@/components/Apanel/Approve/ApproveStudents.vue"),
            meta: { title: "Подтверждения" },
            hidden: true,
          },
          {
            path: "userManagement/",
            name: "userManagement",
            component: () => import("@/components/Apanel/UserManagementComponent.vue"),
            meta: { title: "Управление пользователями" },
            hidden: true,
          },
          {
            path: "roleManagement/",
            name: "roleManagement",
            component: () => import("@/components/Apanel/RoleManagementComponent.vue"),
            meta: { title: "Управление ролями" },
            hidden: true,
          },
          {
            path: "dictionaries/",
            name: "dictionaries",
            component: () => import("@/components/Apanel/Dictionaries/index.vue"),
            meta: { title: "Справочники" },
            hidden: true,
          },
          {
            path: "subjects/",
            name: "subjects",
            component: () => import("@/components/Apanel/SubjectsControl.vue"),
            meta: { title: "Предметы" },
            hidden: true,
          },
        ],
      },
      {
        path: "applications/",
        name: "applications",
        component: () => import("@/views/ApplicantsDocuments/index.vue"),
        meta: { title: "Учет поступления документов", icon: "table", permissions: ["applicants.get.all"] },
      },
      {
        path: "/applicant-homepage/",
        name: "ApplicantHomePage",
        component: () => import("@/views/ApplicantHomePage/index.vue"),
        meta: { title: "Личный кабинет абитуриента", icon: "journal", permissions: ["applicant.applicant.self"] },
      },
    ],
  },

  // 404 page must be placed at the end !!!

  {
    path: "**",
    component: () => import("@/views/404"),
    hidden: true,
  },
];

const createRouter = () => new Router({
  mode: "history", // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes,
});

const router = createRouter();

router.beforeEach((to, from, next) => {
  if (!/\/$/.test(to.path)) {
    next({
      path: `${to.path}/`,
      params: to.params,
      query: to.query,
      replace: true,
    });
  } else {
    next();
  }
});

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter();
  router.matcher = newRouter.matcher; // reset router
}

export default router;
