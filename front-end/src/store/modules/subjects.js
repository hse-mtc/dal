import {
  VuexModule,
  Module,
  Mutation,
  Action,
} from "vuex-module-decorators";
import { Message } from "element-ui";

import store, { SubjectsModule } from "@/store";
import {
  addSection,
  addSubject,
  changeSectionOrder,
  deleteSection,
  deleteSubject,
  editSectionTitle,
  editSubject,
  getSections,
  getSubject,
  getSubjects,
  upsertSubject,
} from "@/api/subjects";
import {
  getAddRequest,
  getDeleteRequest,
  getEditRequest,
  getFetchRequest,
  getOrderChangeRequest,
} from "@/utils/mutators";
import { postError } from "@/utils/message";

@Module({ store, name: "subjects", namespaced: true })
class Subjects extends VuexModule {
  _subjectsList = []
  _subjectsLoaded = false

  subjectId = 0
  _subjectInfo = {}
  _subjectInfoLoaded = false

  _subjectSections = []
  _subjectSectionsLoaded = false

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
      this.$message.error("Не удалось обновить предмет");
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
  SET_SUBJECT_INFO(data) {
    this._subjectInfo = data;
  }

  @Mutation
  SET_SUBJECT_ID(id) {
    this.subjectId = id;
  }

  @Action
  setCurrentSubjectId(id) {
    this.SET_SUBJECT_ID(id);
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
        this.SET_SUBJECT_INFO(data);
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

  @Mutation
  SET_SECTIONS(data) {
    this._subjectSections = data;
  }

  @Action
  async fetchSections() {
    if (!this.subjectId) return false;

    return await getFetchRequest(
      () => getSections(this.subjectId),
      data => {
        this.SET_SECTIONS(data);
        this.SET_IS_LOADED({ field: "_subjectSectionsLoaded", value: true });
      },
      "разделов",
    ).call(this);
  }

  get currentSections() {
    if (!this._subjectSectionsLoaded) {
      SubjectsModule.fetchSections();
    }

    return this._subjectSections;
  }

  @Action
  async updateSectionTitle({ id, ...newData }) {
    getEditRequest(
      editSectionTitle,
      this.SET_SECTIONS,
      "_subjectSections",
      "раздел",
    ).call(this, { id, ...newData });
  }

  @Action
  async addSection(newItem) {
    return await getAddRequest(
      addSection,
      this.SET_SECTIONS,
      "_subjectSections",
      "раздел",
    ).call(this, newItem);
  }

  @Action
  async deleteSection(id) {
    return await getDeleteRequest(
      deleteSection,
      this.SET_SECTIONS,
      "_subjectSections",
      "раздел",
    ).call(this, id);
  }

  @Action
  async changeSectionsOrder({ id, order }) {
    return await getOrderChangeRequest(
      changeSectionOrder,
      this.SET_SECTIONS,
      "_subjectSections",
      "раздела",
    ).call(this, id, order);
  }
}

export default Subjects;
