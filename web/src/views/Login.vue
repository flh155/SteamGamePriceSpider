<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <div class="logo">
          <span class="logo-icon">🎮</span>
          <h1 class="logo-text">Steam 价格追踪</h1>
        </div>
        <p class="subtitle">欢迎回来，请登录您的账户</p>
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
            placeholder="请输入管理员密码"
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
            登录
          </el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { login } from '../api/game'
import { encrypt } from '../utils/crypto'

const router = useRouter()
const formRef = ref(null)
const loading = ref(false)

const form = reactive({
  password: ''
})

const rules = {
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 8, message: '密码长度至少 8 位', trigger: 'blur' }
  ]
}

const handleLogin = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        // 对密码进行加密
        const encryptedPassword = encrypt(form.password)
        
        const response = await login({
          password: encryptedPassword,
          encrypted: true
        })
        
        console.log('Login response:', response)
        
        if (response.code === 200 && response.data && response.data.token) {
          localStorage.setItem('auth_token', response.data.token)
          
          ElMessage.success('登录成功')
          
          // 直接跳转，不使用 setTimeout
          router.replace('/')
        } else {
          const errorMsg = response.message || '登录失败，请检查密码'
          ElMessage.error(errorMsg)
          loading.value = false
        }
      } catch (error) {
        console.error('Login error:', error)
        loading.value = false
        
        let errorMsg = '登录失败，请检查密码'
        
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