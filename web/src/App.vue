<template>
  <div id="app">
    <!-- 仅在非登录/初始化页面显示导航栏 -->
    <nav v-if="!isAuthPage" class="navbar">
      <div class="nav-container">
        <div class="logo">
          <span class="logo-icon">🎮</span>
          <span class="logo-text">{{ t('common.logoText') }}</span>
        </div>
        <div class="nav-links">
          <router-link to="/" class="nav-link active">{{ t('common.home') }}</router-link>
          <a href="#" class="nav-link">{{ t('common.hotGames') }}</a>
          <a href="#" class="nav-link">{{ t('common.about') }}</a>
          <div class="user-actions">
            <!-- 语言切换按钮 -->
            <el-dropdown @command="handleLanguageChange" trigger="click">
              <el-button 
                type="info" 
                size="small" 
                plain
              >
                🌐 {{ currentLocale === 'zh-CN' ? '中文' : 'English' }}
              </el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="zh-CN">🇨🇳 中文</el-dropdown-item>
                  <el-dropdown-item command="en-US">🇺🇸 English</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
            
            <el-button 
              type="info" 
              size="small" 
              @click="goToSettings" 
              plain
            >
              ⚙️ {{ t('common.settings') }}
            </el-button>
            <el-button type="danger" size="small" @click="handleLogout" plain>
              {{ t('common.logout') }}
            </el-button>
          </div>
        </div>
      </div>
    </nav>

    <!-- 主内容区 -->
    <main class="main-content">
      <router-view />
    </main>

    <!-- 页脚 -->
    <footer v-if="!isAuthPage" class="footer">
      <p>{{ t('common.footer') }}</p>
    </footer>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useI18n } from 'vue-i18n'
import { logout } from './api/game'

const router = useRouter()
const route = useRoute()
const { t, locale } = useI18n()

// 当前语言
const currentLocale = computed(() => locale.value)

// 切换语言
const handleLanguageChange = (lang) => {
  locale.value = lang
  localStorage.setItem('locale', lang)
  ElMessage.success(lang === 'zh-CN' ? '语言已切换为中文' : 'Language switched to English')
}

// 判断是否是认证相关页面
const isAuthPage = computed(() => {
  return route.path === '/login' || route.path === '/init-password'
})

// 前往设置页面
const goToSettings = () => {
  router.push('/settings')
}

// 退出登录
const handleLogout = async () => {
  try {
    await logout()
  } catch (error) {
    console.error('Logout error:', error)
  } finally {
    localStorage.removeItem('auth_token')
    ElMessage.success(t('common.success'))
    router.push('/login')
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
  background-color: #1a1f2e;
  color: #e0e0e0;
  min-height: 100vh;
}

#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* 导航栏样式 */
.navbar {
  background: linear-gradient(135deg, #1e2a3a 0%, #2d3a4f 100%);
  border-bottom: 2px solid #3b82f6;
  padding: 1rem 0;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.5rem;
  font-weight: bold;
  color: #3b82f6;
}

.logo-icon {
  font-size: 2rem;
}

.nav-links {
  display: flex;
  gap: 2rem;
  align-items: center;
}

.user-actions {
  margin-left: 1rem;
  display: flex;
  gap: 0.75rem;
}

.nav-link {
  color: #9ca3af;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s ease;
  padding: 0.5rem 1rem;
  border-radius: 6px;
}

.nav-link:hover {
  color: #3b82f6;
  background-color: rgba(59, 130, 246, 0.1);
}

.nav-link.active {
  color: #3b82f6;
  background-color: rgba(59, 130, 246, 0.15);
}

/* 主内容区 */
.main-content {
  flex: 1;
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  width: 100%;
}

/* 页脚 */
.footer {
  background: #1e2a3a;
  border-top: 1px solid #2d3a4f;
  padding: 1.5rem;
  text-align: center;
  color: #6b7280;
  margin-top: auto;
}
</style>