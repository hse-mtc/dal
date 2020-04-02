import request from '@/utils/request'

export function getStudent(params) {
  return request({
    url: '/lms/student/',
    method: 'get',
    params
  })
}

export function putStudent(st) {
  return request({
    url: '/lms/student/',
    method: 'put',
    data: { milgroup : st.milgroup, program: st.program, surname: st.surname, name: st.name, patronymic: st.patronymic, birthdate: st.birthdate, photo: st.photo, status: st.status}
  })
}

export function deleteStudent(id) {
  return request({
    url: '/lms/student/?id='+id,
    method: 'delete'
  })
}
