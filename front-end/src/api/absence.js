import request from '@/utils/request'

export function getAbsence(params) {
  return request({
    url: '/lms/absence/',
    method: 'get',
    params
  })
}
