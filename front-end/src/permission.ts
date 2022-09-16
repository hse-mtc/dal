import NProgress from "nprogress"; // progress bar
import "nprogress/nprogress.css"; // progress bar style

// eslint-disable-next-line import/no-duplicates
import router from "@/router";
import { UserModule } from "@/store";
import getPageTitle from "@/utils/get-page-title";
import { hasPermission } from "@/utils/permissions";
// eslint-disable-next-line import/no-duplicates
import { constantRoutes } from "@/router";

NProgress.configure({ showSpinner: false });

const WHITELIST = ["/login/", "/applicant-form/", "/teacher-registration/", "/student-registration/", "/applicant-registration/"];
const APPLICANTLIST = ["/applicant-registration/", "/applicant-homepage/", "/applicant-form/", "/applicant-to-student/"];

router.beforeEach((to, from, next) => {
  NProgress.start();

  document.title = getPageTitle(to.meta.title);

  if (to.path.includes("change-password")) {
    const access = to.query.token;
    UserModule.SET_TOKENS({ access, refresh: null });
  }

  if (UserModule.accessToken) {
    UserModule.getUser().then(response => {
      if (to.name === "Login") {
        next({ path: "/" });
      }
      const route = constantRoutes.find(elem => elem.path === "/");
      if ((APPLICANTLIST.indexOf(to.path) === -1) && hasPermission(["applicant.applicant.self"]) && !to.path.includes("change-password") && !UserModule.isSuperuser) {
        if (route) {
          route.redirect = "/applicant-homepage/";
        }
        next({ name: "ApplicantHomePage" });
      } else if ((APPLICANTLIST.indexOf(to.path) !== -1) && !hasPermission(["applicant.applicant.self"])) {
        if (route) {
          route.redirect = "/my-materials/";
        }
        next({ path: "/" });
      }
      next();
    });
  } else if (WHITELIST.indexOf(to.path) !== -1) {
    next();
  } else {
    next(`/login/?redirect=${to.path}`);
  }
});

router.afterEach(() => {
  NProgress.done();
});
