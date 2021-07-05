const getters = {
  sidebar: state => state.app.sidebar,
  device: state => state.app.device,
  token: state => state.user.token,
  email: state => state.user.email,
  campuses: state => state.user.campuses,
};
export default getters;
