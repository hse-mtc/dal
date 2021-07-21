import {
  VuexModule,
  Module,
  Mutation,
  Action,
} from "vuex-module-decorators";
import { Message } from "element-ui";

import store, { SubjectsModule } from "@/store";
import {
  addSubject, deleteSubject, editSubject, getSubject, getSubjects, upsertSubject,
} from "@/api/subjects";
import {
  getAddRequest, getDeleteRequest, getEditRequest, getFetchRequest,
} from "@/utils/mutators";

@Module({ store, name: "subjects", namespaced: true })
class Subjects extends VuexModule {
  _subjectsList = []
  _subjectsLoaded = false

  subjectId = 0
  _subjectInfo = {}
  _subjectInfoLoaded = false

  @Mutation
  SET_IS_LOADED({ field, value }) {
    this[field] = value;
  }

  @Mutation
  UPSERT_SUBJECT(payload) {
    const index = this._subjectsList.findIndex(e => e.id === payload.id);

    if (index === -1) {
      this._subjectsList.push(payload);
    } else {
      const tempSubject = this._subjectsList;
      tempSubject[index] = payload;
      this._subjectsList = [...tempSubject];
    }
  }

  @Mutation
  SET_SUBJECTS(payload) {
    this._subjectsList = payload;
  }

  @Action
  async fetchSubjects() {
    return await getFetchRequest(
      getSubjects,
      data => {
        this.SET_SUBJECTS(data);
        this.SET_IS_LOADED({ field: "_subjectsLoaded", value: true });
      },
      "предметов",
    ).call(this);
  }

  @Action
  async addSubject(newItem) {
    return await getAddRequest(
      addSubject,
      this.SET_SUBJECTS,
      "_subjectsList",
      "предмет",
    ).call(this, newItem);
  }

  @Action
  async editSubject({ id, ...newData }) {
    return await getEditRequest(
      editSubject,
      this.SET_SUBJECTS,
      "_subjectsList",
      "предмет",
    ).call(this, { id, ...newData });
  }

  @Action
  async deleteSubject(id) {
    return await getDeleteRequest(
      deleteSubject,
      this.SET_SUBJECTS,
      "_subjectsList",
      "предмет",
    ).call(this, id);
  }

  @Action
  async upsertSubject(newData) {
    try {
      const { data } = await upsertSubject(newData);
      this.UPSERT_SUBJECT(data);
      return true;
    } catch (e) {
      console.error("Не удалось обновить предмет:", e);
      Message({
        type: "error",
        message: "Не удалось обновить предмет",
      });

      return false;
    }
  }

  get subjects() {
    if (!this._subjectsLoaded) {
      SubjectsModule.fetchSubjects();
    }

    return this._subjectsList;
  }

  // Current subject

  @Mutation
  SET_CURRENT_SUBJECT_INFO(data) {
    this._subjectInfo = data;
  }

  @Mutation
  SET_CURRENT_SUBJECT_ID(id) {
    this.subjectId = id;
  }

  @Action
  setCurrentSubjectId(id) {
    this.SET_CURRENT_SUBJECT_ID(id);
    this.SET_IS_LOADED({ field: "_subjectInfoLoaded", value: false });
  }

  @Action
  async fetchSubject() {
    if (!this.subjectId) return false;

    return await getFetchRequest(
      () => getSubject({
        id: this.subjectId,
      }),
      data => {
        this.SET_CURRENT_SUBJECT_INFO(data);
        this.SET_IS_LOADED({ field: "_subjectInfoLoaded", value: true });
      },
      "предмета",
    ).call(this);
  }

  get currentSubject() {
    if (!this._subjectInfoLoaded) {
      SubjectsModule.fetchSubject();
    }

    return this._subjectInfo;
  }
}

export default Subjects;
