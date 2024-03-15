import { request } from '@/api/service'
export const urlPrefix = '/api/system/messages/'
export const urlPrefixOverview = '/api/system/messages_overview/'
export function GetList (query) {
  return request({
    url: urlPrefix,
    method: 'get',
    params: query
  })
}

/**
 * 获取自己接收的消息
 * @param query
 * @returns {*}
 * @constructor
 */
export function GetSelfReceive (query) {
  return request({
    url: urlPrefix + 'get_content/',
    method: 'get',
    params: query
  })
}

export function GetObj (query) {
  return request({
    url: urlPrefixOverview,
    method: 'get',
    params: query
  })
}

export function AddObj (obj) {
  return request({
    url: urlPrefix,
    method: 'post',
    data: obj
  })
}

export function UpdateObj (query) {
  return request({
    url: urlPrefixOverview,
    method: 'put',
    data: query
  })
}
export function DelObj (query) {
  return request({
    url: urlPrefix,
    method: 'delete',
    data: query
  })
}
