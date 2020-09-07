import request from '@/utils/request'

export function getPaperCategories(params) {
  return request({
    url: '/category/',
    method: 'get',
    params
  })
}

export function addPaperCategories(params) {
  return request({
    url: '/category/',
    method: 'put',
    data: {title: params}
  })
}

export function deletePaperCategories(params) {
  return request({
    url: '/category/',
    method: 'delete',
    params
  })
}
