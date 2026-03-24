<template>
  <div class="login-container">
    <!-- 语言切换按钮 -->
    <div class="language-switcher">
      <el-dropdown @command="handleLanguageChange" trigger="click">
        <el-button 
          type="info" 
          size="small" 
          plain
          class="lang-btn"
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
    </div>

    <div class="login-card">
      <div class="login-header">
        <div class="logo">
          <span class="logo-icon">🎮</span>
          <h1 class="logo-text">{{ t('common.logoText') }}</h1>
        </div>
        <p class="subtitle">{{ t('login.welcomeBack') }}</p>
      </div>

      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        class="login-form"
        size="large"
      >
        <el-form-item prop="password">
          <el-input
            v-model="form.password"
            type="password"
            :placeholder="t('login.passwordPlaceholder')"
            show-password
            prefix-icon="Lock"
            @keyup.enter="handleLogin"
          />
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            :loading="loading"
            @click="handleLogin"
            class="login-btn"
          >
            {{ t('login.login') }}
          </el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useI18n } from 'vue-i18n'
import { login } from '../api/game'
import { encrypt, initKeys } from '../utils/crypto'

const router = useRouter()
const formRef = ref(null)
const loading = ref(false)
const { t, locale } = useI18n()

// 当前语言
const currentLocale = computed(() => locale.value)

// 切换语言
const handleLanguageChange = (lang) => {
  locale.value = lang
  localStorage.setItem('locale', lang)
  ElMessage.success(lang === 'zh-CN' ? '语言已切换为中文' : 'Language switched to English')
}

const form = reactive({
  password: ''
})

const rules = {
  password: [
    { required: true, message: t('login.passwordRequired'), trigger: 'blur' },
    { min: 8, message: t('login.passwordMinLength'), trigger: 'blur' }
  ]
}

const handleLogin = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        // 初始化加密密钥
        await initKeys()
        
        // 对密码进行加密
        const encryptedPassword = encrypt(form.password)
        
        const response = await login({
          password: encryptedPassword,
          encrypted: true
        })
        
        console.log('Login response:', response)
        
        if (response.code === 200 && response.data && response.data.token) {
          localStorage.setItem('auth_token', response.data.token)
          
          ElMessage.success(t('login.loginSuccess'))
          
          // 直接跳转，不使用 setTimeout
          router.replace('/')
        } else {
          const errorMsg = response.message || t('login.loginFailed')
          ElMessage.error(errorMsg)
          loading.value = false
        }
      } catch (error) {
        console.error('Login error:', error)
        loading.value = false
        
        let errorMsg = t('login.loginFailed')
        
        if (error.message) {
          errorMsg = error.message
        } else if (error.response && error.response.data) {
          errorMsg = error.response.data.message || errorMsg
        }
        
        ElMessage.error(errorMsg)
      } finally {
        loading.value = false
      }
    }
  })
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #1a1f2e 0%, #2d3a4f 100%);
  padding: 2rem;
  position: relative;
}

/* 语言切换按钮样式 */
.language-switcher {
  position: absolute;
  top: 2rem;
  right: 2rem;
  z-index: 1000;
}

.lang-btn {
  background: rgba(59, 130, 246, 0.1);
  border-color: rgba(59, 130, 246, 0.3);
  color: #3b82f6;
}

.lang-btn:hover {
  background: rgba(59, 130, 246, 0.2);
  border-color: rgba(59, 130, 246, 0.5);
}

.login-card {
  width: 100%;
  max-width: 420px;
  background: rgba(30, 42, 58, 0.95);
  border-radius: 16px;
  padding: 3rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
  border: 1px solid rgba(59, 130, 246, 0.2);
}

.login-header {
  text-align: center;
  margin-bottom: 2.5rem;
}

.logo {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.logo-icon {
  font-size: 2.5rem;
}

.logo-text {
  font-size: 1.8rem;
  font-weight: bold;
  color: #3b82f6;
  margin: 0;
}

.subtitle {
  color: #9ca3af;
  font-size: 1rem;
  margin: 0;
}

.login-form {
  margin-bottom: 2rem;
}

.login-btn {
  width: 100%;
  height: 44px;
  font-size: 1.1rem;
  font-weight: 500;
}
</style>