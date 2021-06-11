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
} from "@/api/reference-book";

const initState = {
  milgroups: [],
  ranks: [],
  studentStatuses: [],
  studentPosts: [],
  teacherPosts: [],
  milfaculties: [],
  milspecialties: [],
  achievementTypes: [],
  programs: [],
  rooms: [],
  absenceTypes: [],
  absenceStatuses: [],
};

const mutations = {
  /* eslint-disable no-param-reassign */
  SET_MILGROUPS: (state, payload) => {
    state.milgroups = payload;
  },
  SET_RANKS: (state, payload) => {
    state.ranks = payload;
  },
  SET_STUDENT_STATUSES: (state, payload) => {
    state.studentStatuses = payload;
  },
  SET_STUDENT_POSTS: (state, payload) => {
    state.studentPosts = payload;
  },
  SET_TEACHER_POSTS: (state, payload) => {
    state.studentPosts = payload;
  },
  SET_MILFACULTIES: (state, payload) => {
    state.milfaculties = payload;
  },
  SET_MILSPECIALTIES: (state, payload) => {
    state.milspecialties = payload;
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
  /* eslint-enable no-param-reassign */
};

const actions = {
  async fetchMilgroups({ commit }) {
    const { data } = await getMilGroups();
    commit("SET_MILGROUPS", data);
  },
  async fetchRanks({ commit }) {
    const { data } = await getRanks();
    commit("SET_RANKS", data);
  },
  async fetchStudentStatuses({ commit }) {
    const data = ["AP", "ST", "EX", "GR"];
    commit("SET_STUDENT_STATUSES", data);
  },
  async fetchStudentPosts({ commit }) {
    const { data } = await getStudentPosts();
    commit("SET_STUDENT_POSTS", data);
  },
  async fetchTeacherPosts({ commit }) {
    const { data } = await getTeacherPosts();
    commit("SET_TEACHER_POSTS", data);
  },
  async fetchMilfaculties({ commit }) {
    const { data } = await getMilFaculties();
    commit("SET_MILFACULTIES", data);
  },
  async fetchMilspecialties({ commit }) {
    const { data } = await getReferenceMilSpecialties();
    commit("SET_MILSPECIALTIES", data);
  },
  async fetchAchievementTypes({ commit }) {
    const { data } = await getAchievementTypes();
    commit("SET_ACHIEVEMENT_TYPES", data);
  },
  async fetchPrograms({ commit }) {
    const { data } = await getPrograms();
    commit("SET_PROGRAMS", data);
  },
  async fetchRooms({ commit }) {
    const { data } = await getRooms();
    commit("SET_ROOMS", data);
  },
  async fetchAbsenceTypes({ commit }) {
    const data = [
      { label: "Уважительная", code: "SE" },
      { label: "Неуважительная", code: "NS" },
      { label: "Опоздание", code: "LA" },
    ];
    commit("SET_ABSENCE_TYPES", data);
  },
  async fetchAbsenceStatuses({ commit }) {
    const data = [
      { label: "Закрыт", code: "CL" },
      { label: "Открыт", code: "OP" },
    ];
    commit("SET_ABSENCE_STATUSES", data);
  },
};

export default {
  namespaced: true,
  state: initState,
  mutations,
  actions,
};
