import request from '@/utils/request'

export function getPublishPlaces(params) {
  return request({
    url: '/published_places',
    method: 'get',
    params
  })
}
