import request from '@/utils/request'

export function getAbsence(params) {
  return request({
    url: '/lms/absence/',
    method: 'get',
    params
  })
}

export function getAbsenceJournal(params) {
  return request({
    url: '/lms/absence_journal/',
    method: 'get',
    params
  })
}
