import request from '@/utils/request'

export function deleteNir(params) {
  return request({
    url: '/delete_nir',
    method: 'get',
    params
  })
}

export function deleteArticle(params) {
  return request({
    url: '/delete_article',
    method: 'get',
    params
  })
}