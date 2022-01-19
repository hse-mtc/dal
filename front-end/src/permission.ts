import NProgress from "nprogress"; // progress bar
import "nprogress/nprogress.css"; // progress bar style

import router from "@/router";
import { UserModule } from "@/store";
import getPageTitle from "@/utils/get-page-title";
import { hasPermission } from "@/utils/permissions";

NProgress.configure({ showSpinner: false });

const WHITELIST = ["/login/", "/applicant-form/", "/register/", "/applicant-registration/"];
const APPLICANTLIST = ["/applicant-registration/", "/applicant-homepage/"];

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
        if (to.name !== "ApplicantHomePage" && hasPermission(["..all"]) && !to.path.includes("change-password") && !UserModule.isSuperuser) {
          console.log("Applicant");
          console.log(!UserModule.isSuperuser);
          next({ name: "ApplicantHomePage" });
        } else if ((APPLICANTLIST.indexOf(to.path) !== -1) && !hasPermission(["..all"])) {
          next({ path: "/" });
        } else {
          console.log("Not an Applicant");
          console.log("otkuda", from.name, "kuda", to.name);
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
