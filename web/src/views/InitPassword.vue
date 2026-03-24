<template>
  <div class="init-password-container">
    <!-- 加载中 -->
    <div v-if="checking" class="loading-card">
      <div class="loading-spinner">⏳</div>
      <p class="loading-text">正在检查初始化状态...</p>
    </div>

    <!-- 已初始化提示 -->
    <div v-else-if="alreadyInitialized" class="initialized-card">
      <div class="initialized-icon">⚠️</div>
      <h2 class="initialized-title">密码已初始化</h2>
      <p class="initialized-message">管理员密码已经完成初始化，无法再次设置。</p>
      <el-button type="primary" @click="goToLogin" class="action-btn">
        前往登录
      </el-button>
    </div>

    <!-- 正常初始化表单 -->
    <div v-else class="init-card">
      <div class="init-header">
        <div class="logo">
          <span class="logo-icon">🎮</span>
          <h1 class="logo-text">Steam 价格追踪</h1>
        </div>
        <p class="subtitle">首次使用，请设置管理员密码</p>
      </div>

      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        class="init-form"
        size="large"
      >
        <el-form-item prop="password">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="请输入管理员密码"
            show-password
            prefix-icon="Lock"
            @input="handlePasswordInput"
          />
        </el-form-item>

        <el-form-item prop="confirmPassword">
          <el-input
            v-model="form.confirmPassword"
            type="password"
            placeholder="请确认管理员密码"
            show-password
            prefix-icon="Lock"
          />
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            :loading="loading"
            @click="handleSubmit"
            class="submit-btn"
          >
            设置密码
          </el-button>
        </el-form-item>
      </el-form>

      <div class="tips-container">
        <div class="tips-card">
          <div class="tips-header">
            <span class="tips-icon">🔒</span>
            <span class="tips-title">密码安全要求</span>
          </div>
          <ul class="tips-list">
            <li>
              <span class="tip-icon">✓</span>
              <span>密码长度至少 8 位，最多 32 位</span>
            </li>
            <li>
              <span class="tip-icon">✓</span>
              <span>必须包含以下四种字符中的至少两种：</span>
            </li>
            <li class="sub-item">
              <span class="tip-dot">•</span>
              <span>大写字母 (A-Z)</span>
            </li>
            <li class="sub-item">
              <span class="tip-dot">•</span>
              <span>小写字母 (a-z)</span>
            </li>
            <li class="sub-item">
              <span class="tip-dot">•</span>
              <span>数字 (0-9)</span>
            </li>
            <li class="sub-item">
              <span class="tip-dot">•</span>
              <span>常用符号 (!@#$%^&*_-+=等)</span>
            </li>
            <li>
              <span class="tip-icon">✗</span>
              <span>不能包含空格、中文或其他特殊字符</span>
            </li>
            <li>
              <span class="tip-icon">✓</span>
              <span>请妥善保管您的密码</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { initPassword } from '../api/game'
import { encrypt } from '../utils/crypto'

const router = useRouter()
const formRef = ref(null)
const loading = ref(false)
const alreadyInitialized = ref(false)
const checking = ref(true)

const form = reactive({
  password: '',
  confirmPassword: ''
})

// 检查是否已初始化
const checkInitialized = async () => {
  try {
    const response = await fetch('http://localhost:5000/api/auth/check-init', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    
    const data = await response.json()
    console.log('Init page check result:', JSON.parse(JSON.stringify(data)))
    
    // 详细检查 initialized 字段
    const isInitialized = data.data?.initialized === true
    console.log('Password initialized status:', isInitialized)
    
    // 只有当后端明确返回 initialized=true 时，才认为是已初始化
    if (isInitialized) {
      console.log('Password already initialized, showing initialized message')
      alreadyInitialized.value = true
    } else {
      console.log('Password not initialized, showing input form')
      alreadyInitialized.value = false
    }
  } catch (error) {
    console.error('Check initialized error:', error)
    // 如果请求失败（后端未启动等），默认视为未初始化
    alreadyInitialized.value = false
  } finally {
    // 重要：确保这里一定会执行
    console.log('Setting checking to false')
    checking.value = false
  }
}

// 处理密码输入，自动过滤不允许的字符
const handlePasswordInput = () => {
  // 移除所有空格
  form.password = form.password.replace(/\s/g, '')
}

// 密码强度验证函数
const validatePasswordStrength = (rule, value, callback) => {
  if (!value || value.length === 0) {
    callback(new Error('请输入密码'))
    return
  }

  // 检查是否包含空格（虽然 input 已经过滤，但双重保险）
  if (/\s/.test(value)) {
    callback(new Error('密码不能包含空格'))
    return
  }

  // 检查是否包含中文字符
  if (/[\u4e00-\u9fa5]/.test(value)) {
    callback(new Error('密码不能包含中文字符'))
    return
  }

  // 检查是否包含其他不允许的特殊字符（只允许常见的英文符号）
  // 使用更安全的字符检查和转义
  const allowedSpecialChars = '!@#$%^&*_-+=.<>?/\\|~`\'"[]{}():;,'
  
  for (let char of value) {
    const isUpperCase = /[A-Z]/.test(char)
    const isLowerCase = /[a-z]/.test(char)
    const isDigit = /\d/.test(char)
    const isAllowedSpecial = allowedSpecialChars.includes(char)
    
    if (!isUpperCase && !isLowerCase && !isDigit && !isAllowedSpecial) {
      callback(new Error(`密码包含不允许的字符：${char}`))
      return
    }
  }

  // 检查长度
  if (value.length < 8) {
    callback(new Error('密码长度至少为 8 位'))
    return
  }

  if (value.length > 32) {
    callback(new Error('密码长度不能超过 32 位'))
    return
  }

  // 检查字符类型 - 使用单独的测试而不是正则字符类
  const hasUpperCase = /[A-Z]/.test(value)
  const hasLowerCase = /[a-z]/.test(value)
  const hasDigits = /\d/.test(value)
  
  // 检查是否包含任何允许的特殊字符
  const hasSpecialChars = value.split('').some(char => allowedSpecialChars.includes(char))

  // 统计满足的条件数量
  const conditionCount = [hasUpperCase, hasLowerCase, hasDigits, hasSpecialChars].filter(Boolean).length

  if (conditionCount < 2) {
    callback(new Error('密码必须包含大写字母、小写字母、数字、特殊符号中的至少两种'))
    return
  }

  callback()
}

const validateConfirmPassword = (rule, value, callback) => {
  if (value !== form.password) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

const rules = {
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { 
      validator: validatePasswordStrength, 
      trigger: 'blur' 
    }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    { validator: validateConfirmPassword, trigger: 'blur' }
  ]
}

const handleSubmit = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        // 对密码进行加密
        const encryptedPassword = encrypt(form.password)
        
        await initPassword({
          password: encryptedPassword,
          encrypted: true
        })
        
        ElMessage.success('密码设置成功，即将跳转到登录页面')
        
        // 使用 replace 而不是 push，避免回退
        setTimeout(() => {
          router.replace('/login')
        }, 1500)
      } catch (error) {
        console.error('Init password error:', error)
        ElMessage.error(error.response?.data?.message || '设置失败，请重试')
      } finally {
        loading.value = false
      }
    }
  })
}

const goToLogin = () => {
  router.push('/login')
}

onMounted(() => {
  console.log('InitPassword page mounted, checking initialized status...')
  checkInitialized()
})
</script>

<style scoped>
.init-password-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #1a1f2e 0%, #2d3a4f 100%);
  padding: 2rem;
}

/* 新增：加载状态样式 */
.loading-card {
  width: 100%;
  max-width: 450px;
  background: rgba(30, 42, 58, 0.95);
  border-radius: 16px;
  padding: 3rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
  border: 1px solid rgba(59, 130, 246, 0.2);
  text-align: center;
  animation: fadeIn 0.3s ease;
}

.loading-spinner {
  font-size: 3rem;
  margin-bottom: 1.5rem;
  animation: pulse 1.5s infinite;
}

.loading-text {
  color: #9ca3af;
  font-size: 1.1rem;
  margin: 0;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.6;
    transform: scale(1.1);
  }
}

.init-card {
  width: 100%;
  max-width: 450px;
  background: rgba(30, 42, 58, 0.95);
  border-radius: 16px;
  padding: 3rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
  border: 1px solid rgba(59, 130, 246, 0.2);
  animation: fadeIn 0.3s ease;
}

/* 已初始化状态卡片 */
.initialized-card {
  width: 100%;
  max-width: 450px;
  background: rgba(30, 42, 58, 0.95);
  border-radius: 16px;
  padding: 3rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
  border: 1px solid rgba(239, 68, 68, 0.3);
  text-align: center;
  animation: slideUp 0.4s ease;
}

.initialized-icon {
  font-size: 4rem;
  margin-bottom: 1.5rem;
  display: block;
}

.initialized-title {
  font-size: 1.8rem;
  font-weight: bold;
  color: #ef4444;
  margin-bottom: 1rem;
  text-shadow: 0 0 20px rgba(239, 68, 68, 0.3);
}

.initialized-message {
  color: #9ca3af;
  font-size: 1.1rem;
  margin-bottom: 2rem;
  line-height: 1.6;
}

.action-btn {
  width: 100%;
  height: 44px;
  font-size: 1.1rem;
  font-weight: 500;
}

.init-header {
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

.init-form {
  margin-bottom: 2rem;
}

.submit-btn {
  width: 100%;
  height: 44px;
  font-size: 1.1rem;
  font-weight: 500;
}

/* 优化后的提示框样式 */
.tips-container {
  margin-top: 1.5rem;
  animation: fadeIn 0.3s ease;
}

.tips-card {
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%);
  border: 1px solid rgba(59, 130, 246, 0.3);
  border-radius: 12px;
  padding: 1.5rem;
  backdrop-filter: blur(10px);
}

.tips-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid rgba(59, 130, 246, 0.2);
}

.tips-icon {
  font-size: 1.5rem;
}

.tips-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #60a5fa;
  text-shadow: 0 0 10px rgba(96, 165, 250, 0.3);
}

.tips-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.tips-list li {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
  color: #e0e7ff;
  font-size: 0.95rem;
  line-height: 1.6;
}

.tips-list li:last-child {
  margin-bottom: 0;
}

.tip-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
  font-size: 0.75rem;
  font-weight: bold;
  flex-shrink: 0;
  margin-top: 2px;
}

.tip-icon:nth-child(odd) {
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
}

.tip-dot {
  display: inline-block;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #60a5fa;
  margin-top: 8px;
  flex-shrink: 0;
}

.sub-item {
  margin-left: 1.5rem !important;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>