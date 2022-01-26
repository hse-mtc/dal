import NProgress from "nprogress"; // progress bar
import "nprogress/nprogress.css"; // progress bar style

import router from "@/router";
import { UserModule } from "@/store";
import getPageTitle from "@/utils/get-page-title";
import { hasPermission } from "@/utils/permissions";

NProgress.configure({ showSpinner: false });

const WHITELIST = ["/login/", "/register/", "/applicant-registration/"];
const APPLICANTLIST = ["/applicant-registration/", "/applicant-homepage/", "/applicant-form/"];

router.beforeEach((to, from, next) => {
  NProgress.start();

  document.title = getPageTitle(to.meta.title);

  if (to.path.includes("change-password")) {
    const access = to.query.token;
    UserModule.SET_TOKENS({ access, refresh: null });
  }

  if (UserModule.accessToken) {
    if (to.name === "Login") {
      next({ path: "/" });
    } else {
      UserModule.getUser().then(response => {
        console.log("person", UserModule.personId, "perm", UserModule.permissions);
        if ((APPLICANTLIST.indexOf(to.path) === -1) && hasPermission(["applicant.applicant.self"]) && !to.path.includes("change-password") && !UserModule.isSuperuser) {
          next({ name: "ApplicantHomePage" });
        } else if ((APPLICANTLIST.indexOf(to.path) !== -1) && !hasPermission(["applicant.applicant.self"])) {
          next({ path: "/" });
        } else {
          next();
        }
      });
    }
  } else if (WHITELIST.indexOf(to.path) !== -1) {
    next();
  } else {
    next(`/login/?redirect=${to.path}`);
  }
});

router.afterEach(() => {
  NProgress.done();
});
