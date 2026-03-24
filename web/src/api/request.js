import axios from 'axios'

const request = axios.create({
  baseURL: 'http://localhost:5000',
  timeout: 30000
})

// 请求拦截器 - 添加 token
request.interceptors.request.use(
  config => {
    const token = localStorage.getItem('auth_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    console.error('Request error:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  response => {
    const res = response.data
    
    // 只有非 /api/auth/login 和 /api/auth/init 接口才检查 code
    const isAuthEndpoint = response.config.url.includes('/api/auth/login') || 
                          response.config.url.includes('/api/auth/init')
    
    // 对于认证接口，直接返回数据，让调用方处理
    if (isAuthEndpoint) {
      return res
    }
    
    // 对于其他接口，检查 code
    if (res.code !== 200) {
      // 401 未授权，跳转到登录页
      if (res.code === 401) {
        localStorage.removeItem('auth_token')
        window.location.href = '/login'
      }
      return Promise.reject(new Error(res.message || 'Error'))
    }
    return res
  },
  error => {
    console.error('API Error:', error)
    
    // 如果是 HTTP 状态码错误（如 401, 403, 500 等）
    if (error.response) {
      const status = error.response.status
      
      // 401 未授权，跳转到登录页（但不要重复跳转）
      if (status === 401 && !window.location.pathname.includes('/login')) {
        localStorage.removeItem('auth_token')
        window.location.href = '/login'
      }
      
      // 返回错误信息给调用方
      return Promise.reject(error.response.data || error)
    }
    
    return Promise.reject(error)
  }
)

export default request