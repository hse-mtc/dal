import Vue from "vue";
import Vuex from "vuex";
import getters from "./getters";
import app from "./modules/app";
import settings from "./modules/settings";
import user from "./modules/user";
import subjects from "./modules/subjects";
import documents from "./modules/documents";

Vue.use(Vuex);

const store = new Vuex.Store({
  modules: {
    app,
    settings,
    user,
    subjects,
    documents,
  },
  getters,
});

export default store;
