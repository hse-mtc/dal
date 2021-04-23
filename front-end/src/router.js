import Vue from "vue";
import Router from "vue-router";

Vue.use(Router);

/* Layout */
import Layout from "@/layout";

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
    name: "SignUp",
    path: "/register/",
    component: () => import("@/views/Signup/index"),
    hidden: true,
  },
  {
    path: "/change-password/",
    component: () => import("@/views/ChangePassword/index"),
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
        path: "msw/science-articles/",
        name: "Science Articles",
        component: () => import("@/views/ScienceArticles/index"),
        meta: { title: "Военно-научные работы", icon: "study" },
      },

      {
        path: "subjects/",
        name: "Subjects",
        component: () => import("@/views/Subjects/index"),
        meta: { title: "Учебно-методические материалы", icon: "book" },
      },
      {
        path: "subjects/:subjectId/",
        hidden: true,
        name: "Subject",
        component: () => import("@/views/Subject/index"),
        meta: { title: "Учебно-методические материалы" },
      },

      {
        path: "library/",
        name: "Library",
        component: () => import("@/views/Library/index"),
        meta: { title: "Электронная библиотека", icon: "books" },
      },
      {
        path: "library/book/:id/",
        name: "Book",
        component: () => import("@/views/Book/index"),
        meta: { title: "Электронная библиотека" },
        hidden: true,
      },

      {
        path: "personnel/",
        name: "Personnel",
        component: () => import("@/views/Personnel/index"),
        meta: { title: "Личный состав ВУЦ", icon: "people" },
      },

      {
        path: "absence/",
        name: "Absence",
        component: () => import("@/views/Absence/index"),
        meta: { title: "Журнал посещаемости", icon: "session-log" },
      },

      {
        path: "discipline/",
        name: "Discipline",
        component: () => import("@/views/Discipline/index"),
        meta: { title: "Дисциплинарная практика", icon: "cross" },
      },

      {
        path: "schedule/",
        name: "Schedule",
        component: () => import("@/views/Schedule/index"),
        meta: { title: "Расписание занятий", icon: "calendar" },
      },

      {
        path: "marks/",
        name: "Marks",
        component: () => import("@/views/Marks/index"),
        meta: { title: "Журнал оценок", icon: "journal" },
      },

      {
        path: "apanel/",
        name: "AdminPanel",
        component: () => import("@/views/AdminPanel/index"),
        meta: { title: "Панель администратора", icon: "journal" },
      },

      {
        path: "applications/",
        name: "applications",
        component: () => import("@/views/ApplicantsDocuments/index.vue"),
        meta: { title: "Учет поступления документов", icon: "table" },
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

const createRouter = () =>
  new Router({
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
