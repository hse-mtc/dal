import Vue from "vue";
import Vuex from "vuex";
import { getModule } from "vuex-module-decorators";
import app from "./modules/app";
import settings from "./modules/settings";
import user from "./modules/user";
import subjects from "./modules/subjects";
import papers from "./modules/papers";
import reference from "./modules/reference";

Vue.use(Vuex);

const store = new Vuex.Store({
  modules: {
    app,
    settings,
    user,
    subjects,
    papers,
    reference,
  },
});

export default store;

export const AppModule = getModule(app, store);
export const PapersModule = getModule(papers, store);
export const ReferenceModule = getModule(reference, store);
export const SettingsModule = getModule(settings, store);
export const SubjectsModule = getModule(subjects, store);
export const UserModule = getModule(user, store);
