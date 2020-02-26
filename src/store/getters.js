const getters = {
  sidebar: state => state.app.sidebar,
  device: state => state.app.device,
  token: state => state.user.token,
  name: state => state.user.name,
  subjects: state => state.projectData.subjects,
  publishers: state => state.documents.publishers,
  authors: state => state.documents.authors,
}
export default getters
