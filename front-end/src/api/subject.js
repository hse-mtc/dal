import request from '@/utils/request'

export function getSubject(params) {
  return request({
    url: '/dms/subject/',
    method: 'get',
    params
  })
}
