const initState = {
  subjects: [],
};

const mutations = {
  /* eslint-disable no-param-reassign */
  UPSERT_SUBJECT: (state, payload) => {
    const index = state.subjects.findIndex(e => e.id === payload.id);

    if (index === -1) {
      state.subjects.push(payload);
    } else {
      const tempSubject = state.subjects;
      tempSubject[index] = payload;
      state.subjects = [...tempSubject];
    }
  },
  SET_SUBJECTS: (state, payload) => {
    state.subjects = payload;
  },
  DELETE_SUBJECT: (state, id) => {
    state.subjects = state.subjects.filter(subject => subject.id !== id);
  },
};

const actions = {
  setSubjects({ commit }, subjects) {
    commit("SET_SUBJECTS", subjects);
  },
  deleteSubject({ commit }, id) {
    commit("DELETE_SUBJECT", id);
  },
  upsertSubject({ commit }, subject) {
    commit("UPSERT_SUBJECT", subject);
  },
};

export default {
  namespaced: true,
  state: initState,
  mutations,
  actions,
};
