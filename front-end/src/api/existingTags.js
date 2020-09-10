import request from '@/utils/request'

export function getExistingTags(params) {
  return request({
    url: '/dms/tags/',
    method: 'get',
    params
  })
}
