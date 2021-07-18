import {
  VuexModule,
  Module,
  Mutation,
  Action,
} from "vuex-module-decorators";

import store, { ReferenceModule } from "@/store";

import {
  getMilFaculties,
  getMilGroups,
  getStudentPosts,
  getTeacherPosts,
  getRanks,
  getAchievementTypes,
  getPrograms,
  getRooms,
  getSkills,
  addMilGroup,
  deleteMilGroup,
  editMilGroup,
  addAchievementType,
  editAchievementType,
  addMilFaculty,
  editMilFaculty,
  getMilSpecialties,
  addMilSpecialty,
  editMilSpecialty,
  deleteMilSpecialty,
  addProgram,
  editProgram,
  deleteProgram,
  addRank,
  editRank,
  deleteRank,
} from "@/api/reference-book";
import {
  getAddRequest,
  getDeleteRequest,
  getEditRequest,
  getFetchRequest,
} from "@/utils/mutators";
import { getError } from "@/utils/message";

@Module({ store, name: "reference", namespaced: true })
class Reference extends VuexModule {
  _milgroups = [];
  _milgroupsLoaded = false;

  _ranks = [];
  _ranksLoaded = false;

  _studentStatuses = [];
  _studentStatusesLoaded = false;

  _studentPosts = [];
  _studentPostsLoaded = false;

  _teacherPosts = [];
  _teacherPostsLoaded = false;

  _milfaculties = [];
  _milfacultiesLoaded = false;

  _milspecialties = [];
  _milspecialtiesLoaded = false;

  _achievementTypes = [];
  _achievementTypesLoaded = false;

  _programs = [];
  _programsLoaded = false;

  _rooms = [];
  _roomsLoaded = false;

  _absenceTypes = [];
  _absenceTypesLoaded = false;

  _absenceStatuses = [];
  _absenceStatusesLoaded = false;

  _skills = [];
  _skillsLoaded = false;

  @Mutation
  SET_IS_LOADED({ field, value }) {
    this[field] = value;
  }

  // MILGROUPS
  @Mutation
  SET_MILGROUPS(payload) {
    this._milgroups = payload;
  }

  @Action
  async fetchMilgroups() {
    return await getFetchRequest(
      getMilGroups,
      data => {
        this.SET_MILGROUPS(data);
        this.SET_IS_LOADED({ field: "_milgroupsLoaded", value: true });
      },
      "взвода",
    ).call(this);
  }

  @Action
  async addMilgroup(newItem) {
    return await getAddRequest(
      addMilGroup,
      this.SET_MILGROUPS,
      "_milgroups",
      "взвод",
    ).call(this, newItem);
  }

  @Action
  async editMilgroup({ id, ...newData }) {
    return await getEditRequest(
      editMilGroup,
      this.SET_MILGROUPS,
      "_milgroups",
      "взвод",
    ).call(this, { id, ...newData });
  }

  @Action
  async deleteMilgroup(id) {
    return await getDeleteRequest(
      deleteMilGroup,
      this.SET_MILGROUPS,
      "_milgroups",
      "взвод",
    ).call(this, id);
  }

  get milgroups() {
    if (!this._milgroupsLoaded) {
      ReferenceModule.fetchMilgroups();
    }

    return this._milgroups;
  }

  // RANKS
  @Mutation
  SET_RANKS(payload) {
    this._ranks = payload;
  }

  @Action
  async fetchRanks() {
    return await getFetchRequest(
      getRanks,
      data => {
        this.SET_RANKS(data);
        this.SET_IS_LOADED({ field: "_ranksLoaded", value: true });
      },
      "званий",
    ).call(this);
  }

  @Action
  async addRank(newItem) {
    return await getAddRequest(
      addRank,
      this.SET_RANKS,
      "_ranks",
      "звание",
    ).call(this, newItem);
  }

  @Action
  async editRank({ id, ...newData }) {
    return await getEditRequest(
      editRank,
      this.SET_RANKS,
      "_ranks",
      "звание",
    ).call(this, { id, ...newData });
  }

  @Action
  async deleteRank(id) {
    return await getDeleteRequest(
      deleteRank,
      this.SET_RANKS,
      "_ranks",
      "звание",
    ).call(this, id);
  }

  get ranks() {
    if (!this._ranksLoaded) {
      ReferenceModule.fetchRanks();
    }

    return this._ranks;
  }

  // STUDENTS STATUSES
  @Mutation
  SET_STUDENT_STATUSES(payload) {
    this._studentStatuses = payload;
  }

  @Action({ commit: "SET_STUDENT_STATUSES" })
  async setStudentStatuses(studentStatuses) {
    return studentStatuses;
  }

  @Action
  async fetchStudentStatuses() {
    try {
      const data = [
        { code: "ST", label: "Обучающийся" },
        { code: "EX", label: "Отчислен" },
        { code: "GR", label: "Выпустился" },
      ];
      this.setStudentStatuses(data);
      this.SET_IS_LOADED({ field: "_studentStatusesLoaded", value: true });
    } catch (err) {
      getError("статусов студентов", err.response.status);
    }
  }

  get studentStatuses() {
    if (!this._studentStatusesLoaded) {
      ReferenceModule.fetchStudentStatuses();
    }

    return this._studentStatuses;
  }

  // STUDENT POSTS
  @Mutation
  SET_STUDENT_POSTS(payload) {
    this._studentPosts = payload;
  }

  @Action({ commit: "SET_STUDENT_POSTS" })
  async setStudentPosts(studentPosts) {
    return studentPosts;
  }

  @Action
  async fetchStudentPosts() {
    try {
      const { data } = await getStudentPosts();
      this.setStudentPosts(data);
      this.SET_IS_LOADED({ field: "_studentPostsLoaded", value: true });
    } catch (err) {
      getError("должностей студентов", err.response.status);
    }
  }

  get studentPosts() {
    if (!this._studentPostsLoaded) {
      ReferenceModule.fetchStudentPosts();
    }

    return this._studentPosts;
  }

  // TEACHER POSTS
  @Mutation
  SET_TEACHER_POSTS(payload) {
    this._teacherPosts = payload;
  }

  @Action({ commit: "SET_TEACHER_POSTS" })
  async setTeacherPosts(teacherPosts) {
    return teacherPosts;
  }

  @Action
  async fetchTeacherPosts() {
    try {
      const { data } = await getTeacherPosts();
      this.setTeacherPosts(data);
      this.SET_IS_LOADED({ field: "_teacherPostsLoaded", value: true });
    } catch (err) {
      getError("должностей преподавателей", err.response.status);
    }
  }

  get teacherPosts() {
    if (!this._teacherPostsLoaded) {
      ReferenceModule.fetchTeacherPosts();
    }

    return this._teacherPosts;
  }

  // MILFACULTIES
  @Mutation
  SET_MILFACULTIES(payload) {
    this._milfaculties = payload;
  }

  @Action
  async fetchMilfaculties() {
    return await getFetchRequest(
      getMilFaculties,
      data => {
        this.SET_MILFACULTIES(data);
        this.SET_IS_LOADED({ field: "_milfacultiesLoaded", value: true });
      },
      "циклов",
    ).call(this);
  }

  @Action
  async addMilfaculty(newItem) {
    return await getAddRequest(
      addMilFaculty,
      this.SET_MILFACULTIES,
      "_milfaculties",
      "цикла",
    ).call(this, newItem);
  }

  @Action
  async editMilfaculty({ id, ...newData }) {
    return await getEditRequest(
      editMilFaculty,
      this.SET_MILFACULTIES,
      "_milfaculties",
      "цикла",
    ).call(this, { id, ...newData });
  }

  @Action
  async deleteMilfaculty(id) {
    return await getDeleteRequest(
      deleteMilGroup,
      this.SET_MILFACULTIES,
      "_milfaculties",
      "цикла",
    ).call(this, id);
  }

  get milfaculties() {
    if (!this._milfacultiesLoaded) {
      ReferenceModule.fetchMilfaculties();
    }

    return this._milfaculties;
  }

  // milspecialties
  @Mutation
  SET_MILSPECIALTIES(payload) {
    this._milspecialties = payload;
  }

  @Action
  async fetchMilSpecialties() {
    return await getFetchRequest(
      getMilSpecialties,
      data => {
        this.SET_MILSPECIALTIES(data);
        this.SET_IS_LOADED({ field: "_milspecialtiesLoaded", value: true });
      },
      "воинских специальностей",
    ).call(this);
  }

  @Action
  async addMilSpecialty(newItem) {
    return await getAddRequest(
      addMilSpecialty,
      this.SET_MILSPECIALTIES,
      "_milspecialties",
      "воинскую специальность",
    ).call(this, newItem);
  }

  @Action
  async editMilSpecialty({ id, ...newData }) {
    return await getEditRequest(
      editMilSpecialty,
      this.SET_MILSPECIALTIES,
      "_milspecialties",
      "воинскую специальность",
    ).call(this, { id, ...newData });
  }

  @Action
  async deleteMilSpecialty(id) {
    return await getDeleteRequest(
      deleteMilSpecialty,
      this.SET_MILSPECIALTIES,
      "_milspecialties",
      "воинскую специальность",
    ).call(this, id);
  }

  get milspecialties() {
    if (!this._milspecialtiesLoaded) {
      ReferenceModule.fetchMilSpecialties();
    }

    return this._milspecialties;
  }

  // ACHIEVEMENT TYPES
  @Mutation
  SET_ACHIEVEMENT_TYPES(payload) {
    this._achievementTypes = payload;
  }

  @Action
  async fetchAchievementTypes() {
    return await getFetchRequest(
      getAchievementTypes,
      data => {
        this.SET_ACHIEVEMENT_TYPES(data);
        this.SET_IS_LOADED({ field: "_achievementTypesLoaded", value: true });
      },
      "типов достижений",
    ).call(this);
  }

  @Action
  async addAchievementType(newItem) {
    return await getAddRequest(
      addAchievementType,
      this.SET_ACHIEVEMENT_TYPES,
      "_achievementTypes",
      "тип достижения",
    ).call(this, newItem);
  }

  @Action
  async editAchievementType({ id, ...newData }) {
    return await getEditRequest(
      editAchievementType,
      this.SET_ACHIEVEMENT_TYPES,
      "_achievementTypes",
      "тип достижения",
    ).call(this, { id, ...newData });
  }

  @Action
  async deleteAchievementType(id) {
    return await getDeleteRequest(
      deleteMilGroup,
      this.SET_ACHIEVEMENT_TYPES,
      "_achievementTypes",
      "тип достижения",
    ).call(this, id);
  }

  get achievementTypes() {
    if (!this._achievementTypesLoaded) {
      ReferenceModule.fetchAchievementTypes();
    }

    return this._achievementTypes;
  }

  // PROGRAMS
  @Mutation
  SET_PROGRAMS(payload) {
    this._programs = payload;
  }

  @Action
  async fetchPrograms() {
    return await getFetchRequest(
      getPrograms,
      data => {
        this.SET_PROGRAMS(data);
        this.SET_IS_LOADED({ field: "_programsLoaded", value: true });
      },
      "образовательных программ",
    ).call(this);
  }

  @Action
  async addProgram(newItem) {
    return await getAddRequest(
      addProgram,
      this.SET_PROGRAMS,
      "_programs",
      "образовательную программу",
    ).call(this, newItem);
  }

  @Action
  async editProgram({ id, ...newData }) {
    return await getEditRequest(
      editProgram,
      this.SET_PROGRAMS,
      "_programs",
      "образовательную программу",
    ).call(this, { id, ...newData });
  }

  @Action
  async deleteProgram(id) {
    return await getDeleteRequest(
      deleteProgram,
      this.SET_PROGRAMS,
      "_programs",
      "образовательную программу",
    ).call(this, id);
  }

  get programs() {
    if (!this._programsLoaded) {
      ReferenceModule.fetchPrograms();
    }

    return this._programs;
  }

  // ROOMS
  @Mutation
  SET_ROOMS(payload) {
    this._rooms = payload;
  }

  @Action({ commit: "SET_ROOMS" })
  async setRooms(rooms) {
    return rooms;
  }

  @Action
  async fetchRooms() {
    try {
      const { data } = await getRooms();
      this.setRooms(data);
      this.SET_IS_LOADED({ field: "_roomsLoaded", value: true });
    } catch (err) {
      getError("аудиторий", err.response.status);
    }
  }

  get rooms() {
    if (!this._roomsLoaded) {
      ReferenceModule.fetchRooms();
    }

    return this._rooms;
  }

  // ABSENCE TYPES
  @Mutation
  SET_ABSENCE_TYPES(payload) {
    this._absenceTypes = payload;
  }

  @Action({ commit: "SET_ABSENCE_TYPES" })
  async setAbsenceTypes(absenceTypes) {
    return absenceTypes;
  }

  @Action
  async fetchAbsenceTypes() {
    try {
      const data = [
        { label: "Уважительная", code: "SE" },
        { label: "Неуважительная", code: "NS" },
        { label: "Опоздание", code: "LA" },
      ];
      this.setAbsenceTypes(data);
      this.SET_IS_LOADED({ field: "_absenceTypesLoaded", value: true });
    } catch (err) {
      getError("типов пропусков", err.response.status);
    }
  }

  get absenceTypes() {
    if (!this._absenceTypesLoaded) {
      ReferenceModule.fetchAbsenceTypes();
    }

    return this._absenceTypes;
  }

  // ABSENCE STATUSES
  @Mutation
  SET_ABSENCE_STATUSES(payload) {
    this._absenceStatuses = payload;
  }

  @Action({ commit: "SET_ABSENCE_STATUSES" })
  async setAbsenceStatuses(absenceStatuses) {
    return absenceStatuses;
  }

  @Action
  async fetchAbsenceStatuses() {
    try {
      const data = [
        { label: "Закрыт", code: "CL" },
        { label: "Открыт", code: "OP" },
      ];
      this.setAbsenceStatuses(data);
      this.SET_IS_LOADED({ field: "_absenceStatusesLoaded", value: true });
    } catch (err) {
      getError("статусов пропусков", err.response.status);
    }
  }

  get absenceStatuses() {
    if (!this._absenceStatusesLoaded) {
      ReferenceModule.fetchAbsenceStatuses();
    }

    return this._absenceStatuses;
  }

  // SKILLS
  @Mutation
  SET_SKILLS(payload) {
    this._skills = payload;
  }

  @Action({ commit: "SET_SKILLS" })
  async setSkills(skills) {
    return skills;
  }

  @Action
  async fetchSkills() {
    try {
      const { data } = await getSkills();
      this.setSkills(data);
      this.SET_IS_LOADED({ field: "_skillsLoaded", value: true });
    } catch (err) {
      getError("умений", err.response.status);
    }
  }

  get skills() {
    if (!this._skillsLoaded) {
      ReferenceModule.fetchSkills();
    }

    return this._skills;
  }
}

export default Reference;
