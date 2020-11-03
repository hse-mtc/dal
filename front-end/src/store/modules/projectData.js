const state = {
  subjects: [],
};

const mutations = {
  SET_SUBJECTS: (state, payload) => {
    state.subjects = payload;
  },
};

const actions = {
  addSubjects({ commit }, subjects) {
    commit("SET_SUBJECTS", subjects);
  },
};

export default {
  namespaced: true,
  state,
  mutations,
  actions,
};
