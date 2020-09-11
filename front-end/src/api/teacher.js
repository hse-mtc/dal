import request from '@/utils/request'

export function getTeacher(params) {
  return request({
    url: '/lms/teacher/',
    method: 'get',
    params
  })
}

export function putTeacher(st) {
  return request({
    url: '/lms/teacher/',
    method: 'put',
    data: { milgroup : st.milgroup, program: st.program, surname: st.surname, name: st.name, patronymic: st.patronymic, birthdate: st.birthdate, photo: st.photo, status: st.status}
  })
}

export function postTeacher(st) {
  return request({
    url: '/lms/teacher/',
    method: 'post',
    data: { id: st.id, milgroup : st.milgroup, program: st.program, surname: st.surname, name: st.name, patronymic: st.patronymic, birthdate: st.birthdate, photo: st.photo, status: st.status}
  })
}

export function deleteTeacher(id) {
  return request({
    url: '/lms/teacher/?id='+id,
    method: 'delete'
  })
}
