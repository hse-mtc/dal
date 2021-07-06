import {
  VuexModule,
  Module,
  Mutation,
  Action,
} from "vuex-module-decorators";

import store from "@/store";

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

@Module({ store, name: "reference", namespaced: true })
class Reference extends VuexModule {
  milgroups = []
  ranks = []
  studentStatuses = []
  studentPosts = []
  teacherPosts = []
  milfaculties = []
  milspecialties = []
  achievementTypes = []
  programs = []
  rooms = []
  absenceTypes = []
  absenceStatuses = []
  skills = []

  @Mutation
  SET_MILGROUPS(payload) {
    this.milgroups = payload;
  }

  @Mutation
  SET_RANKS(payload) {
    this.ranks = payload;
  }

  @Mutation
  SET_STUDENT_STATUSES(payload) {
    this.studentStatuses = payload;
  }

  @Mutation
  SET_STUDENT_POSTS(payload) {
    this.studentPosts = payload;
  }

  @Mutation
  SET_TEACHER_POSTS(payload) {
    this.studentPosts = payload;
  }

  @Mutation
  SET_MILFACULTIES(payload) {
    this.milfaculties = payload;
  }

  @Mutation
  SET_MILSPECIALTIES(payload) {
    this.milspecialties = payload;
  }

  @Mutation
  SET_ACHIEVEMENT_TYPES(payload) {
    this.achievementTypes = payload;
  }

  @Mutation
  SET_PROGRAMS(payload) {
    this.programs = payload;
  }

  @Mutation
  SET_ROOMS(payload) {
    this.rooms = payload;
  }

  @Mutation
  SET_ABSENCE_TYPES(payload) {
    this.absenceTypes = payload;
  }

  @Mutation
  SET_ABSENCE_STATUSES(payload) {
    this.absenceStatuses = payload;
  }

  @Mutation
  SET_SKILLS(payload) {
    this.skills = payload;
  }

  @Action({ commit: "SET_MILGROUPS" })
  async fetchMilgroups() {
    return (await getMilGroups()).data;
  }

  @Action({ commit: "SET_RANKS" })
  async fetchRanks() {
    return (await getRanks()).data;
  }

  @Action({ commit: "SET_STUDENT_STATUSES" })
  async fetchStudentStatuses() {
    return ["AP", "ST", "EX", "GR"];
  }

  @Action({ commit: "SET_STUDENT_POSTS" })
  async fetchStudentPosts() {
    return (await getStudentPosts()).data;
  }

  @Action({ commit: "SET_TEACHER_POSTS" })
  async fetchTeacherPosts() {
    return (await getTeacherPosts()).data;
  }

  @Action({ commit: "SET_MILFACULTIES" })
  async fetchMilfaculties() {
    return (await getMilFaculties()).data;
  }

  @Action({ commit: "SET_MILSPECIALTIES" })
  async fetchMilspecialties() {
    return (await getReferenceMilSpecialties()).data;
  }

  @Action({ commit: "SET_ACHIEVEMENT_TYPES" })
  async fetchAchievementTypes() {
    return (await getAchievementTypes()).data;
  }

  @Action({ commit: "SET_PROGRAMS" })
  async fetchPrograms() {
    return (await getPrograms()).data;
  }

  @Action({ commit: "SET_ROOMS" })
  async fetchRooms() {
    return (await getRooms()).data;
  }

  @Action({ commit: "SET_SKILLS" })
  async fetchSkills() {
    return (await getSkills()).data;
  }

  @Action({ commit: "SET_ABSENCE_TYPES" })
  async fetchAbsenceTypes() {
    const data = [
      { label: "Уважительная", code: "SE" },
      { label: "Неуважительная", code: "NS" },
      { label: "Опоздание", code: "LA" },
    ];

    return data;
  }

  @Action({ commit: "SET_ABSENCE_STATUSES" })
  async fetchAbsenceStatuses() {
    const data = [
      { label: "Закрыт", code: "CL" },
      { label: "Открыт", code: "OP" },
    ];

    return data;
  }
}

export default Reference;
