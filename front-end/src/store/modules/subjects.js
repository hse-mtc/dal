import {
  VuexModule,
  Module,
  Mutation,
  Action,
} from "vuex-module-decorators";
import { Message } from "element-ui";

import store, { SubjectsModule, UserModule } from "@/store";
import { deleteSubject, getSubjects, upsertSubject } from "@/api/subjects";

@Module({ store, name: "subjects", namespaced: true })
class Subjects extends VuexModule {
  _subjectsList = []
  _subjectsLoaded = false

  @Mutation
  SET_IS_LOADED(value) {
    this._subjectsLoaded = value;
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

  @Action({ commit: "SET_SUBJECTS" })
  setSubjects(subjects) {
    return subjects;
  }

  @Action
  async fetchSubjects() {
    try {
      const { data } = await getSubjects();
      this.setSubjects(data);
      this.SET_IS_LOADED(true);
    } catch (e) {
      console.error("Не удалось загрузить данные предментов");
      Message({
        type: "error",
        message: "Не удалось загрузить данные предментов",
      });
    }
  }

  @Action
  async deleteSubject(id) {
    try {
      await deleteSubject(id);

      this.setSubjects(this._subjectsList.filter(item => item.id !== id));

      return true;
    } catch (e) {
      console.error("Не удалось удалить предмет:", e);
      Message({
        type: "error",
        message: "Не удалось удалить предмет",
      });

      return false;
    }
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
}

export default Subjects;
