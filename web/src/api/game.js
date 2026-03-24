import request from './request'

export function getGamePrice(gameName) {
  return request({
    url: '/api/game/search',
    method: 'get',
    params: { game_name: gameName }
  })
}

export function getHotGames(num = 20) {
  return request({
    url: '/api/game/hot',
    method: 'get',
    params: { num }
  })
}

// 初始化密码
export function initPassword(data) {
  return request({
    url: '/api/auth/init',
    method: 'post',
    data
  })
}

// 登录
export function login(data) {
  return request({
    url: '/api/auth/login',
    method: 'post',
    data
  })
}

// 检查认证状态
export function checkAuth() {
  return request({
    url: '/api/auth/check',
    method: 'get'
  })
}

// 登出
export function logout() {
  return request({
    url: '/api/auth/logout',
    method: 'post'
  })
}

// 获取 API KEY
export function getApiKey() {
  return request({
    url: '/api/settings/api-key',
    method: 'get'
  })
}

// 设置 API KEY
export function setApiKey(data) {
  return request({
    url: '/api/settings/api-key',
    method: 'post',
    data
  })
}

// 修改密码
export function changePassword(data) {
  return request({
    url: '/api/settings/change-password',
    method: 'post',
    data
  })
}