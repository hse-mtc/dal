const initState = {
  publishers: [],
  authors: [],
  categories: [],
};

const mutations = {
  /* eslint-disable no-param-reassign */
  SET_AUTHORS: (state, payload) => {
    state.authors = payload;
  },
  SET_PUBLISHERS: (state, payload) => {
    state.publishers = payload;
  },
  SET_CATEGORIES: (state, payload) => {
    state.categories = payload;
  },
  /* eslint-enable no-param-reassign */
};

const actions = {
  setCategories({ commit }, categories) {
    commit("SET_CATEGORIES", categories);
  },
  setAuthors({ commit }, authors) {
    return new Promise(resolve => {
      commit("SET_AUTHORS", authors);
      resolve();
    });
  },
  setPublishers({ commit }, publishers) {
    return new Promise(resolve => {
      commit("SET_PUBLISHERS", publishers);
      resolve();
    });
  },
};

export default {
  namespaced: true,
  state: initState,
  mutations,
  actions,
};
