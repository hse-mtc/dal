import { Message } from "element-ui";
import NProgress from "nprogress"; // progress bar
import "nprogress/nprogress.css"; // progress bar style
import getPageTitle from "@/utils/get-page-title";
import LocalStorageService from "@/utils/LocalStorageService";

import router from "./router";

const localStorageService = LocalStorageService.getService();

NProgress.configure({ showSpinner: false }); // NProgress Configuration

// no redirect whitelist
const whiteList = ["/login/", "/applicant-form/", "/register/"];

router.beforeEach(async(to, from, next) => {
  // start progress bar
  NProgress.start();

  // set page title
  document.title = getPageTitle(to.meta.title);

  // determine whether the user has logged in
  const hasToken = localStorageService.getAccessToken();

  if (hasToken) {
    if (to.path === "/login") {
      // if is logged in, redirect to the home page
      next({ path: "/" });
      NProgress.done();
    } else {
      next();
    }
    /* has no token */
  } else if (whiteList.indexOf(to.path) !== -1) {
    // in the free login whitelist, go directly
    next();
  } else {
    // other pages that do not have permission to access are redirected to the login page.
    next(`/login/?redirect=${to.path}`);
    NProgress.done();
  }
});

router.afterEach(() => {
  // finish progress bar
  NProgress.done();
});
