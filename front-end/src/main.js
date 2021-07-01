import Vue from "vue";

import moment from "moment";
import FunctionalCalendar from "vue-functional-calendar";
import BootstrapVue from "bootstrap-vue";
import "normalize.css/normalize.css"; // A modern alternative to CSS resets
import Multiselect from "vue-multiselect";
import VueLodash from "vue-lodash";
import lodash from "lodash";
import VueMeta from "vue-meta";

import "@/styles/index.scss"; // global css

import App from "./App.vue";
import store from "./store";
import router from "./router";

import "@/icons"; // icon
import "@/permission"; // permission control
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";

import "./elementUIApply";
import "./primeApply";

Vue.component("Multiselect", Multiselect);

Vue.use(VueMeta);
Vue.use(VueLodash, { name: "custom", lodash });

Vue.prototype.$moment = moment;

moment.locale("ru");

Vue.use(BootstrapVue);
Vue.use(FunctionalCalendar, {
  dayNames: ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"],
  monthNames: [
    "Январь",
    "Февраль",
    "Март",
    "Апрель",
    "Май",
    "Июнь",
    "Июль",
    "Август",
    "Сентябрь",
    "Октябрь",
    "Ноябрь",
    "Декабрь",
  ],
  shortMonthNames: [
    "Янв",
    "Февр",
    "Март",
    "Апр",
    "Май",
    "Июнь",
    "Июль",
    "Авг",
    "Сент",
    "Окт",
    "Ноя",
    "Дек",
  ],
});

Vue.config.productionTip = false;

// eslint-disable-next-line no-new
new Vue({
  el: "#app",
  router,
  store,
  render: h => h(App),
});
