<template>
  <div class="settings-container">
    <div class="settings-card">
      <h1 class="settings-title">⚙️ 系统设置</h1>
      
      <!-- API Key 设置 -->
      <div class="settings-section">
        <div class="section-header">
          <span class="section-icon">🔑</span>
          <h2 class="section-title">API 配置</h2>
        </div>
        
        <el-form
          ref="apiKeyFormRef"
          :model="apiKeyForm"
          :rules="apiKeyRules"
          label-position="top"
        >
          <el-form-item label="IsThereAnyDeal API Key" prop="apiKey">
            <el-input
              v-model="apiKeyForm.apiKey"
              type="password"
              placeholder="请输入你的 API Key"
              show-password
              clearable
            />
            <div class="form-tip">
              ℹ️ API Key 用于查询 Steam 游戏价格数据，请妥善保管<br>
              💡 你可以在 <a href="https://isthereanydeal.com/apps/" target="_blank">IsThereAnyDeal API 官网</a> 获取
            </div>
          </el-form-item>
          
          <el-form-item>
            <el-button
              type="primary"
              :loading="savingApiKey"
              @click="handleSaveApiKey"
            >
              保存 API Key
            </el-button>
          </el-form-item>
        </el-form>
      </div>

      <!-- 修改密码 -->
      <div class="settings-section">
        <div class="section-header">
          <span class="section-icon">🔒</span>
          <h2 class="section-title">修改登录密码</h2>
        </div>
        
        <el-form
          ref="passwordFormRef"
          :model="passwordForm"
          :rules="passwordRules"
          label-position="top"
        >
          <el-form-item label="当前密码" prop="oldPassword">
            <el-input
              v-model="passwordForm.oldPassword"
              type="password"
              placeholder="请输入当前密码"
              show-password
            />
          </el-form-item>
          
          <el-form-item label="新密码" prop="newPassword">
            <el-input
              v-model="passwordForm.newPassword"
              type="password"
              placeholder="请输入新密码"
              show-password
              @input="handleNewPasswordInput"
            />
            <div class="form-tip">
              密码要求：8-32 位，包含大小写字母、数字、特殊符号中的至少两种
            </div>
          </el-form-item>
          
          <el-form-item label="确认新密码" prop="confirmPassword">
            <el-input
              v-model="passwordForm.confirmPassword"
              type="password"
              placeholder="请再次输入新密码"
              show-password
            />
          </el-form-item>
          
          <el-form-item>
            <el-button
              type="warning"
              :loading="changingPassword"
              @click="handleChangePassword"
            >
              修改密码并重新登录
            </el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getApiKey, setApiKey, changePassword as apiChangePassword } from '../api/game'
import { encrypt } from '../utils/crypto'

const router = useRouter()

// API Key 相关
const apiKeyFormRef = ref(null)
const savingApiKey = ref(false)

const apiKeyForm = reactive({
  apiKey: ''
})

const apiKeyRules = {
  apiKey: [
    { required: true, message: '请输入 API Key', trigger: 'blur' }
  ]
}

// 加载 API Key
const loadApiKey = async () => {
  try {
    const response = await getApiKey()
    if (response.code === 200 && response.data && response.data.api_key) {
      apiKeyForm.apiKey = response.data.api_key
    }
  } catch (error) {
    console.error('Load API Key error:', error)
    ElMessage.error('加载 API Key 失败')
  }
}

// 保存 API Key
const handleSaveApiKey = async () => {
  if (!apiKeyFormRef.value) return
  
  await apiKeyFormRef.value.validate(async (valid) => {
    if (valid) {
      savingApiKey.value = true
      try {
        // 对 API Key 进行加密
        const encryptedApiKey = encrypt(apiKeyForm.apiKey)
        
        await setApiKey({
          api_key: encryptedApiKey,
          encrypted: true
        })
        ElMessage.success('API Key 保存成功')
      } catch (error) {
        console.error('Save API Key error:', error)
        ElMessage.error(error.response?.data?.message || '保存失败，请重试')
      } finally {
        savingApiKey.value = false
      }
    }
  })
}

// 修改密码相关
const passwordFormRef = ref(null)
const changingPassword = ref(false)

const passwordForm = reactive({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

// 处理新密码输入，自动过滤空格
const handleNewPasswordInput = () => {
  passwordForm.newPassword = passwordForm.newPassword.replace(/\s/g, '')
}

// 密码强度验证
const validatePasswordStrength = (rule, value, callback) => {
  if (!value || value.length === 0) {
    callback(new Error('请输入密码'))
    return
  }

  if (/\s/.test(value)) {
    callback(new Error('密码不能包含空格'))
    return
  }

  if (/[\u4e00-\u9fa5]/.test(value)) {
    callback(new Error('密码不能包含中文字符'))
    return
  }

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

  if (value.length < 8) {
    callback(new Error('密码长度至少为 8 位'))
    return
  }

  if (value.length > 32) {
    callback(new Error('密码长度不能超过 32 位'))
    return
  }

  const hasUpperCase = /[A-Z]/.test(value)
  const hasLowerCase = /[a-z]/.test(value)
  const hasDigits = /\d/.test(value)
  const hasSpecialChars = value.split('').some(char => allowedSpecialChars.includes(char))

  const conditionCount = [hasUpperCase, hasLowerCase, hasDigits, hasSpecialChars].filter(Boolean).length

  if (conditionCount < 2) {
    callback(new Error('密码必须包含大写字母、小写字母、数字、特殊符号中的至少两种'))
    return
  }

  callback()
}

const validateConfirmPassword = (rule, value, callback) => {
  if (value !== passwordForm.newPassword) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

const passwordRules = {
  oldPassword: [
    { required: true, message: '请输入当前密码', trigger: 'blur' }
  ],
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { validator: validatePasswordStrength, trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认新密码', trigger: 'blur' },
    { validator: validateConfirmPassword, trigger: 'blur' }
  ]
}

// 修改密码
const handleChangePassword = async () => {
  if (!passwordFormRef.value) return
  
  await passwordFormRef.value.validate(async (valid) => {
    if (valid) {
      changingPassword.value = true
      try {
        // 对密码进行加密
        const encryptedOldPassword = encrypt(passwordForm.oldPassword)
        const encryptedNewPassword = encrypt(passwordForm.newPassword)
        const encryptedConfirmPassword = encrypt(passwordForm.confirmPassword)
        
        await apiChangePassword({
          old_password: encryptedOldPassword,
          new_password: encryptedNewPassword,
          confirm_password: encryptedConfirmPassword,
          encrypted: true
        })
        
        ElMessage.success('密码修改成功，请重新登录')
        
        localStorage.removeItem('auth_token')
        setTimeout(() => {
          router.push('/login')
        }, 1500)
      } catch (error) {
        console.error('Change password error:', error)
        ElMessage.error(error.response?.data?.message || '修改失败，请重试')
      } finally {
        changingPassword.value = false
      }
    }
  })
}

onMounted(() => {
  loadApiKey()
})
</script>

<style scoped>
.settings-container {
  display: flex;
  justify-content: center;
  min-height: calc(100vh - 200px);
  padding: 2rem;
}

.settings-card {
  width: 100%;
  max-width: 700px;
  background: rgba(30, 42, 58, 0.95);
  border-radius: 16px;
  padding: 3rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
  border: 1px solid rgba(59, 130, 246, 0.2);
}

.settings-title {
  font-size: 2rem;
  font-weight: bold;
  color: #3b82f6;
  margin-bottom: 2.5rem;
  text-align: center;
}

.settings-section {
  margin-bottom: 3rem;
  padding-bottom: 3rem;
  border-bottom: 1px solid rgba(59, 130, 246, 0.2);
}

.settings-section:last-child {
  margin-bottom: 0;
  padding-bottom: 0;
  border-bottom: none;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}

.section-icon {
  font-size: 1.8rem;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #e0e7ff;
  margin: 0;
}

.form-tip {
  margin-top: 0.75rem;
  font-size: 0.85rem;
  color: #9ca3af;
  line-height: 1.8;
}

.form-tip a {
  color: #60a5fa;
  text-decoration: none;
}

.form-tip a:hover {
  text-decoration: underline;
}

:deep(.el-form-item__label) {
  color: #e0e7ff !important;
  font-weight: 500;
}

:deep(.el-input__wrapper) {
  background: rgba(15, 23, 42, 0.6);
  border-color: rgba(59, 130, 246, 0.3);
}

:deep(.el-input__inner) {
  color: #e0e7ff;
}

:deep(.el-button--primary) {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  border: none;
}

:deep(.el-button--warning) {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  border: none;
}
</style>