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
    st
  })
}
