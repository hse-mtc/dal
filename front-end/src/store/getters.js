const getters = {
  sidebar: state => state.app.sidebar,
  device: state => state.app.device,
  token: state => state.user.token,
  email: state => state.user.email,
  campuses: state => state.user.campuses,
  subjects: state => state.subjects.subjects,
};
export default getters;
