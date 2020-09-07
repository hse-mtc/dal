import request from '@/utils/request'

export function getExistingTags(params) {
  return request({
    url: '/get_tags/',
    method: 'get',
    params
  })
}
