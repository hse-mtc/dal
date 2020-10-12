import request from '@/utils/request'

export function getDocuments(category, authors, published_places, start_date, end_date, text) {
  return request({
    url: '/dms/papers/',
    method: 'get',
    params : {category: category, authors: authors, publishers: published_places, start_date: start_date, end_date: end_date, search: text}
  })
}
