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
  getReferenceMilSpecialties,
  getAchievementTypes,
  getPrograms,
  getRooms,
  getSkills,
} from "@/api/reference-book";
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

  @Action({ commit: "SET_MILGROUPS" })
  setMilgroups(milgroups) {
    return milgroups;
  }

  @Action()
  async fetchMilgroups() {
    try {
      const { data } = await getMilGroups();
      this.setMilgroups(data);
      this.SET_IS_LOADED({ field: "_milgroupsLoaded", value: true });
    } catch (err) {
      getError("взводов", err.response.status);
    }
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

  @Action({ commit: "SET_RANKS" })
  async setRanks(ranks) {
    return ranks;
  }

  @Action()
  async fetchRanks() {
    try {
      const { data } = await getRanks();
      this.setRanks(data);
      this.SET_IS_LOADED({ field: "_ranksLoaded", value: true });
    } catch (err) {
      getError("званий", err.response.status);
    }
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
      const data = ["AP", "ST", "EX", "GR"];
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

  @Action({ commit: "SET_MILFACULTIES" })
  async setMilfaculties(milfaculties) {
    return milfaculties;
  }

  @Action
  async fetchMilfaculties() {
    try {
      const { data } = await getMilFaculties();
      this.setMilfaculties(data);
      this.SET_IS_LOADED({ field: "_milfacultiesLoaded", value: true });
    } catch (err) {
      getError("циклов", err.response.status);
    }
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

  @Action({ commit: "SET_MILSPECIALTIES" })
  async setmilspecialties(milspecialties) {
    return milspecialties;
  }

  @Action
  async fetchmilspecialties() {
    try {
      const { data } = await getReferenceMilSpecialties();
      console.log("🚀 > data", data);
      this.setmilspecialties(data);
      this.SET_IS_LOADED({ field: "_milspecialtiesLoaded", value: true });
    } catch (err) {
      getError("воинских специальностей", err.response.status);
    }
  }

  get milspecialties() {
    if (!this._milspecialtiesLoaded) {
      ReferenceModule.fetchmilspecialties();
    }

    return this._milspecialties;
  }

  // ACHIEVEMENT TYPES
  @Mutation
  SET_ACHIEVEMENT_TYPES(payload) {
    this._achievementTypes = payload;
  }

  @Action({ commit: "SET_ACHIEVEMENT_TYPES" })
  async setAchievementTypes(achievementTypes) {
    return achievementTypes;
  }

  @Action
  async fetchAchievementTypes() {
    try {
      const { data } = await getAchievementTypes();
      this.setAchievementTypes(data);
      this.SET_IS_LOADED({ field: "_achievementTypesLoaded", value: true });
    } catch (err) {
      getError("типов достижений", err.response.status);
    }
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

  @Action({ commit: "SET_PROGRAMS" })
  async setPrograms(programs) {
    return programs;
  }

  @Action
  async fetchPrograms() {
    try {
      const { data } = await getPrograms();
      this.setPrograms(data);
      this.SET_IS_LOADED({ field: "_programsLoaded", value: true });
    } catch (err) {
      getError("образовательных программ", err.response.status);
    }
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
