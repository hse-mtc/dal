const getters = {
  sidebar: (state) => state.app.sidebar,
  device: (state) => state.app.device,
  token: (state) => state.user.token,
  email: (state) => state.user.email,
  subjects: (state) => state.subjects.subjects,
  publishers: (state) => state.documents.publishers,
  authors: (state) => state.documents.authors,
  categories: (state) => state.documents.categories,
};
export default getters;
