import { Message } from "element-ui";
import NProgress from "nprogress"; // progress bar
import "nprogress/nprogress.css"; // progress bar style
import getPageTitle from "@/utils/get-page-title";

import router from "./router";
import { UserModule } from "./store";

NProgress.configure({ showSpinner: false });

const whiteList = ["/login/", "/applicant-form/", "/register/"];

router.beforeEach(async(to, from, next) => {
  NProgress.start();

  document.title = getPageTitle(to.meta.title);

  if (to.path.includes("change-password")) {
    const access = to.query.token;
    UserModule.SET_TOKENS({ access, refresh: null });
  }

  if (UserModule.accessToken) {
    if (to.path === "/login") {
      next({ path: "/" });
      NProgress.done();
    } else {
      next();
    }
  } else if (whiteList.indexOf(to.path) !== -1) {
    next();
  } else {
    next(`/login/?redirect=${to.path}`);
    NProgress.done();
  }
});

router.afterEach(() => {
  NProgress.done();
});
