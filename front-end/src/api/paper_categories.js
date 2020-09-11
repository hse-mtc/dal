import request from '@/utils/request'

export function getPaperCategories(params) {
  return request({
    url: '/dms/categories/',
    method: 'get',
    params
  })
}

export function addPaperCategories(params) {
  return request({
    url: '/dms/categories/',
    method: 'put',
    data: {title: params}
  })
}

export function deletePaperCategories(params) {
  return request({
    url: '/dms/categories/',
    method: 'delete',
    params
  })
}
