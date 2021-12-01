import {
  VuexModule, Module, Mutation, Action,
} from "vuex-module-decorators";

import store, { ChoicesModule } from "@/store";

import * as choices from "@/api/choices";

import { getFetchRequest } from "@/utils/mutators";

@Module({ store, name: "choices", namespaced: true })
class Choices extends VuexModule {
  _absenceExcuses = null;
  _absenceStatuses = null;
  _encouragementTypes = null;
  _lessonTypes = null;
  _punishmentTypes = null;
  _studentPosts = null;
  _studentStatuses = null;
  _teacherPosts = null;
  _teacherRanks = null;

  @Mutation
  SET_CHOICES({ name, data }) {
    this[name] = data;
  }

  @Action
  async fetchChoices({ fetchFunc, name, errorMsg }) {
    return await getFetchRequest(
      fetchFunc,
      data => this.SET_CHOICES({ name, data }),
      errorMsg,
    ).call(this);
  }

  get absenceExcuses() {
    if (this._absenceExcuses !== null) {
      return new Promise(resolve => {
        resolve(this._absenceExcuses);
      });
    }

    return ChoicesModule.fetchChoices({
      fetchFunc: choices.fetchAbsenceExcuses,
      name: "_absenceExcuses",
      errorMsg: "причины пропусков",
    }).then(() => this._absenceExcuses);
  }

  get absenceStatuses() {
    if (this._absenceStatuses !== null) {
      return new Promise(resolve => {
        resolve(this._absenceStatuses);
      });
    }

    return ChoicesModule.fetchChoices({
      fetchFunc: choices.fetchAbsenceStatuses,
      name: "_absenceStatuses",
      errorMsg: "статусы пропусков",
    }).then(() => this._absenceStatuses);
  }

  get encouragementTypes() {
    if (this._encouragementTypes !== null) {
      return new Promise(resolve => {
        resolve(this._encouragementTypes);
      });
    }

    return ChoicesModule.fetchChoices({
      fetchFunc: choices.fetchEncouragementTypes,
      name: "_encouragementTypes",
      errorMsg: "типы поощрений",
    }).then(() => this._encouragementTypes);
  }

  get lessonTypes() {
    if (this._lessonTypes !== null) {
      return new Promise(resolve => {
        resolve(this._lessonTypes);
      });
    }

    return ChoicesModule.fetchChoices({
      fetchFunc: choices.fetchLessonTypes,
      name: "_lessonTypes",
      errorMsg: "типы занятий",
    }).then(() => this._lessonTypes);
  }

  get punishmentTypes() {
    if (this._punishmentTypes !== null) {
      return new Promise(resolve => {
        resolve(this._punishmentTypes);
      });
    }

    return ChoicesModule.fetchChoices({
      fetchFunc: choices.fetchPunishmentTypes,
      name: "_punishmentTypes",
      errorMsg: "типы взысканий",
    }).then(() => this._punishmentTypes);
  }

  get studentPosts() {
    if (this._studentPosts !== null) {
      return new Promise(resolve => {
        resolve(this._studentPosts);
      });
    }

    return ChoicesModule.fetchChoices({
      fetchFunc: choices.fetchStudentPosts,
      name: "_studentPosts",
      errorMsg: "должности студентов",
    }).then(() => this._studentPosts);
  }

  get studentStatuses() {
    if (this._studentStatuses !== null) {
      return new Promise(resolve => {
        resolve(this._studentStatuses);
      });
    }

    return ChoicesModule.fetchChoices({
      fetchFunc: choices.fetchStudentStatuses,
      name: "_studentStatuses",
      errorMsg: "статусы студентов",
    }).then(() => this._studentStatuses);
  }

  get teacherPosts() {
    if (this._teacherPosts !== null) {
      return new Promise(resolve => {
        resolve(this._teacherPosts);
      });
    }

    return ChoicesModule.fetchChoices({
      fetchFunc: choices.fetchTeacherPosts,
      name: "_teacherPosts",
      errorMsg: "должности преподавателей",
    }).then(() => this._teacherPosts);
  }

  get teacherRanks() {
    if (this._teacherRanks !== null) {
      return new Promise(resolve => {
        resolve(this._teacherRanks);
      });
    }

    return ChoicesModule.fetchChoices({
      fetchFunc: choices.fetchTeacherRanks,
      name: "_teacherRanks",
      errorMsg: "звания преподавателей",
    }).then(() => this._teacherRanks);
  }
}

export default Choices;
