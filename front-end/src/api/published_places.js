import request from '@/utils/request'

export function getPublishPlaces(params) {
  return request({
    url: '/publishers/',
    method: 'get',
    params
  })
}
