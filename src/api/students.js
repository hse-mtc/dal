import request from '@/utils/request'

export function getStudents(params) {
  return request({
    url: '/students',
    method: 'get',
    params
  })
}
