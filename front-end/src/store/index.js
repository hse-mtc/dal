import Vue from "vue";

import Vuex from "vuex";
import { getModule } from "vuex-module-decorators";

import app from "./modules/app";
import choices from "./modules/choices";
import papers from "./modules/papers";
import reference from "./modules/reference";
import settings from "./modules/settings";
import subjects from "./modules/subjects";
import user from "./modules/user";

Vue.use(Vuex);

const store = new Vuex.Store({
  modules: {
    app,
    choices,
    papers,
    reference,
    settings,
    subjects,
    user,
  },
});

export default store;

export const AppModule = getModule(app, store);
export const ChoicesModule = getModule(choices, store);
export const PapersModule = getModule(papers, store);
export const ReferenceModule = getModule(reference, store);
export const SettingsModule = getModule(settings, store);
export const SubjectsModule = getModule(subjects, store);
export const UserModule = getModule(user, store);
