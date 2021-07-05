import Vue from "vue";
import Vuex from "vuex";
import { getModule } from "vuex-module-decorators";
import getters from "./getters";
import app from "./modules/app";
import settings from "./modules/settings";
import user from "./modules/user";
import subjects from "./modules/subjects";
import documents from "./modules/documents";
import reference from "./modules/reference";

Vue.use(Vuex);

const store = new Vuex.Store({
  modules: {
    app,
    settings,
    user,
    subjects,
    documents,
    reference,
  },
  getters,
});

export default store;

export const AppModule = getModule(app, store);
export const DocumentsModule = getModule(documents, store);
export const ReferenceModule = getModule(reference, store);
export const SettingsModule = getModule(settings, store);
export const SubjectsModule = getModule(subjects, store);
