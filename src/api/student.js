import request from '@/utils/request'

export function getStudent(params) {
  return request({
    url: '/lms/student/',
    method: 'get',
    params
  })
}
