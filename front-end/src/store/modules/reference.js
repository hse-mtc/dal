import { getMilFaculties, getMilGroups, getPosts, getRanks, getReferenceMilSpecialties, getAchievementTypes, getPrograms, getRooms } from "@/api/reference-book";

const state = {
  milgroups: [],
  ranks: [],
  posts: [],
  milfaculties: [],
  milspecialties: [],
  achievementTypes: [],
  programs: [],
  rooms: [],
  absenceTypes: [],
  absenceStatuses: [],
};

const mutations = {
  SET_MILGROUPS: (state, payload) => {
    state.milgroups = payload;
  },
  SET_RANKS: (state, payload) => {
    state.ranks = payload;
  },
  SET_POSTS: (state, payload) => {
    state.posts = payload;
  },
  SET_MILFACULTIES: (state, payload) => {
    state.milfaculties = payload;
  },
  SET_MILSPECIALITIES: (state, payload) => {
    state.achievementTypes = payload;
  },
  SET_ACHIEVEMENT_TYPES: (state, payload) => {
    state.achievementTypes = payload;
  },
  SET_PROGRAMS: (state, payload) => {
    state.programs = payload;
  },
  SET_ROOMS: (state, payload) => {
    state.rooms = payload;
  },
  SET_ABSENCE_TYPES: (state, payload) => {
    state.absenceTypes = payload;
  },
  SET_ABSENCE_STATUSES: (state, payload) => {
    state.absenceStatuses = payload;
  },
};

const actions = {
  async setMilgroups({ commit }) {
    const data = (await getMilGroups()).data;
    commit("SET_MILGROUPS", data);
  },
  async setRanks({ commit }) {
    const data = (await getRanks()).data;
    commit("SET_RANKS", data);
  },
  async setPosts({ commit }) {
    const data = (await getPosts()).data;
    commit("SET_POSTS", data);
  },
  async setMilfaculties({ commit }) {
    const data = (await getMilFaculties()).data;
    commit("SET_MILFACULTIES", data);
  },
  async setMilspecialities({ commit }) {
    const data = (await getReferenceMilSpecialties()).data;
    commit("SET_MILSPECIALITIES", data);
  },
  async setAchievementTypes({ commit }) {
    const data = (await getAchievementTypes()).data;
    commit("SET_ACHIEVEMENT_TYPES", data);
  },
  async setPrograms({ commit }) {
    const data = (await getPrograms()).data;
    commit("SET_PROGRAMS", data);
  },
  async setRooms({ commit }) {
    const data = (await getRooms()).data;
    commit("SET_ROOMS", data);
  },
  async setAbsenceTypes({ commit }) {
    const data = [
      { label: "Уважительная", code: "SE" },
      { label: "Неуважительная", code: "NS" },
      { label: "Опоздание", code: "LA" },
    ];
    commit("SET_ABSENCE_TYPES", data);
  },
  async setAbsenceStatuses({ commit }) {
    const data = [
      { label: "Закрыт", code: "CL" },
      { label: "Открыт", code: "OP" },
    ];
    commit("SET_ABSENCE_STATUSES", data);
  },
};

export default {
  namespaced: true,
  state,
  mutations,
  actions,
};
