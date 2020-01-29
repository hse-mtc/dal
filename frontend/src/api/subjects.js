import request from '@/utils/request'

export function getSubjects(params) {
  return request({
    url: '/subjects',
    method: 'get',
    params
  })
}
