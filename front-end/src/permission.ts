import NProgress from "nprogress"; // progress bar
import "nprogress/nprogress.css"; // progress bar style

import router from "@/router";
import { UserModule } from "@/store";
import getPageTitle from "@/utils/get-page-title";

NProgress.configure({ showSpinner: false });

const WHITELIST = ["/login/", "/applicant-form/", "/register/", "/applicant-registration/"];

router.beforeEach((to, from, next) => {
  NProgress.start();

  document.title = getPageTitle(to.meta.title);

  if (to.path.includes("change-password")) {
    const access = to.query.token;
    UserModule.SET_TOKENS({ access, refresh: null });
  }

  if (UserModule.accessToken) {
    if (to.path === "/login") {
      next({ path: "/" });
    } else {
      next();
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
