import request from '@/utils/request'

export function getTeacher(params) {
  return request({
    url: '/lms/teacher/',
    method: 'get',
    params
  })
}

export function putTeacher(data) {
  return request({
    url: '/lms/teacher/',
    method: 'put',
    data
  })
}

export function postTeacher(data) {
  return request({
    url: '/lms/teacher/'+data.id,
    method: 'post',
    data
  })
}

export function deleteTeacher(id) {
  return request({
    url: '/lms/teacher/'+id,
    method: 'delete'
  })
}
