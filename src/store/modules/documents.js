const state = {
  publishers: [],
  authors: [],
}

const mutations = {
  SET_AUTHORS: (state, payload) => {
    state.authors = payload;
  },
  SET_PUBLISHERS: (state, payload) => {
    state.publishers = payload;
  },
}

const actions = {
}

export default {
  state,
  mutations,
  actions
}
