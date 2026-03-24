import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue')
  },
  {
    path: '/init-password',
    name: 'InitPassword',
    component: () => import('../views/InitPassword.vue')
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('../views/Settings.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 全局路由守卫 - 检查认证状态
router.beforeEach(async (to, from, next) => {
  const token = localStorage.getItem('auth_token')
  const isAuthPage = to.path === '/init-password' || to.path === '/login'
  
  console.log('Route guard triggered:', {
    path: to.path,
    hasToken: !!token,
    isAuthPage,
    from: from.path
  })
  
  // 如果是访问认证相关页面，直接放行
  if (isAuthPage) {
    // 但如果已有 token，且是从登录页跳转过来的，允许去首页
    if (token && from.path === '/login') {
      console.log('Has token and from login page, allowing navigation')
      next()
    } else {
      console.log('Auth page, allowing access')
      next()
    }
    return
  }
  
  // 如果没有 token，先检查是否已初始化密码
  if (!token) {
    console.log('No token, checking init status...')
    try {
      // 调用后端接口检查是否已初始化
      const response = await fetch('http://localhost:5000/api/auth/check-init', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      })
      
      const data = await response.json()
      console.log('Check init status response:', data)
      
      if (data.code === 200 && !data.data.initialized) {
        // 未初始化，强制跳转到初始化页面
        console.log('Password not initialized, redirect to /init-password')
        next('/init-password')
      } else {
        // 已初始化但未登录，跳转到登录页面
        console.log('Password initialized but no token, redirect to /login')
        next('/login')
      }
    } catch (error) {
      console.error('Check init status error:', error)
      // 如果检查失败（后端未启动等），默认跳转到登录页
      next('/login')
    }
  } else {
    // 有 token，允许访问
    console.log('Has token, allowing access')
    next()
  }
})

export default router