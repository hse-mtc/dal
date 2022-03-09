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

const WHITELIST = ["/login/", "/register/", "/applicant-registration/"];
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
      if ((APPLICANTLIST.indexOf(to.path) === -1) && hasPermission(["applicant.applicant.self"]) && !to.path.includes("change-password") && !UserModule.isSuperuser) {
        let counter = 0;
        while (counter < constantRoutes.length) {
          if (constantRoutes[counter].path === "/") {
            constantRoutes[counter].redirect = "/applicant-homepage/";
          }
          // eslint-disable-next-line no-plusplus
          counter++;
        }
        next({ name: "ApplicantHomePage" });
      } else if ((APPLICANTLIST.indexOf(to.path) !== -1) && !hasPermission(["applicant.applicant.self"])) {
        let counter = 0;
        while (counter < constantRoutes.length) {
          if (constantRoutes[counter].path === "/") {
            constantRoutes[counter].redirect = "/my-materials/";
          }
          // eslint-disable-next-line no-plusplus
          counter++;
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
