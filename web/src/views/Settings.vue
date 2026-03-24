<template>
  <div class="settings-container">
    <div class="settings-card">
      <h1 class="settings-title">{{ t('settings.title') }}</h1>
      
      <!-- API Key 设置 -->
      <div class="settings-section">
        <div class="section-header">
          <span class="section-icon">🔑</span>
          <h2 class="section-title">{{ t('settings.apiConfig') }}</h2>
        </div>
        
        <el-form
          ref="apiKeyFormRef"
          :model="apiKeyForm"
          :rules="apiKeyRules"
          label-position="top"
        >
          <el-form-item :label="t('settings.apiKeyLabel')" prop="apiKey">
            <el-input
              v-model="apiKeyForm.apiKey"
              type="password"
              :placeholder="t('settings.apiKeyPlaceholder')"
              show-password
              clearable
            />
            <div class="form-tip">
              ℹ️ {{ t('settings.apiKeyTip1') }}<br>
              💡 <a href="https://isthereanydeal.com/apps/" target="_blank">{{ t('settings.apiKeyTip2') }}</a>
            </div>
          </el-form-item>
          
          <el-form-item>
            <el-button
              type="primary"
              :loading="savingApiKey"
              @click="handleSaveApiKey"
            >
              {{ t('settings.saveApiKey') }}
            </el-button>
          </el-form-item>
        </el-form>
      </div>

      <!-- 修改密码 -->
      <div class="settings-section">
        <div class="section-header">
          <span class="section-icon">🔒</span>
          <h2 class="section-title">{{ t('settings.changePassword') }}</h2>
        </div>
        
        <el-form
          ref="passwordFormRef"
          :model="passwordForm"
          :rules="passwordRules"
          label-position="top"
        >
          <el-form-item :label="t('settings.currentPassword')" prop="oldPassword">
            <el-input
              v-model="passwordForm.oldPassword"
              type="password"
              :placeholder="t('settings.currentPasswordPlaceholder')"
              show-password
            />
          </el-form-item>
          
          <el-form-item :label="t('settings.newPassword')" prop="newPassword">
            <el-input
              v-model="passwordForm.newPassword"
              type="password"
              :placeholder="t('settings.newPasswordPlaceholder')"
              show-password
              @input="handleNewPasswordInput"
            />
            <div class="form-tip">
              {{ t('settings.passwordRequirement') }}
            </div>
          </el-form-item>
          
          <el-form-item :label="t('settings.confirmPassword')" prop="confirmPassword">
            <el-input
              v-model="passwordForm.confirmPassword"
              type="password"
              :placeholder="t('settings.confirmPasswordPlaceholder')"
              show-password
            />
          </el-form-item>
          
          <el-form-item>
            <el-button
              type="warning"
              :loading="changingPassword"
              @click="handleChangePassword"
            >
              {{ t('settings.changePasswordAndRelogin') }}
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
import { useI18n } from 'vue-i18n'
import { getApiKey, setApiKey, changePassword as apiChangePassword } from '../api/game'
import { encrypt, initKeys } from '../utils/crypto'

const router = useRouter()
const { t } = useI18n()

// API Key 相关
const apiKeyFormRef = ref(null)
const savingApiKey = ref(false)

const apiKeyForm = reactive({
  apiKey: ''
})

const apiKeyRules = {
  apiKey: [
    { required: true, message: t('settings.passwordRequired'), trigger: 'blur' }
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
    ElMessage.error(t('common.error'))
  }
}

// 保存 API Key
const handleSaveApiKey = async () => {
  if (!apiKeyFormRef.value) return
  
  await apiKeyFormRef.value.validate(async (valid) => {
    if (valid) {
      savingApiKey.value = true
      try {
        // 初始化加密密钥
        await initKeys()
        
        // 对 API Key 进行加密
        const encryptedApiKey = encrypt(apiKeyForm.apiKey)
        
        await setApiKey({
          api_key: encryptedApiKey,
          encrypted: true
        })
        ElMessage.success(t('settings.saveApiKeySuccess'))
      } catch (error) {
        console.error('Save API Key error:', error)
        ElMessage.error(error.response?.data?.message || t('common.error'))
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
    callback(new Error(t('settings.passwordRequired')))
    return
  }

  if (/\s/.test(value)) {
    callback(new Error(t('settings.passwordNoSpace')))
    return
  }

  if (/[\u4e00-\u9fa5]/.test(value)) {
    callback(new Error(t('settings.passwordNoChinese')))
    return
  }

  const allowedSpecialChars = '!@#$%^&*_-+=.<>?/\\|~`\'"[]{}():;,'
  
  for (let char of value) {
    const isUpperCase = /[A-Z]/.test(char)
    const isLowerCase = /[a-z]/.test(char)
    const isDigit = /\d/.test(char)
    const isAllowedSpecial = allowedSpecialChars.includes(char)
    
    if (!isUpperCase && !isLowerCase && !isDigit && !isAllowedSpecial) {
      callback(new Error(`${t('common.error')}: ${char}`))
      return
    }
  }

  if (value.length < 8) {
    callback(new Error(t('settings.passwordMinLength')))
    return
  }

  if (value.length > 32) {
    callback(new Error(t('settings.passwordMaxLength')))
    return
  }

  const hasUpperCase = /[A-Z]/.test(value)
  const hasLowerCase = /[a-z]/.test(value)
  const hasDigits = /\d/.test(value)
  const hasSpecialChars = value.split('').some(char => allowedSpecialChars.includes(char))

  const conditionCount = [hasUpperCase, hasLowerCase, hasDigits, hasSpecialChars].filter(Boolean).length

  if (conditionCount < 2) {
    callback(new Error(t('settings.passwordStrength')))
    return
  }

  callback()
}

const validateConfirmPassword = (rule, value, callback) => {
  if (value !== passwordForm.newPassword) {
    callback(new Error(t('settings.passwordNotMatch')))
  } else {
    callback()
  }
}

const passwordRules = {
  oldPassword: [
    { required: true, message: t('settings.passwordRequired'), trigger: 'blur' }
  ],
  newPassword: [
    { required: true, message: t('settings.passwordRequired'), trigger: 'blur' },
    { validator: validatePasswordStrength, trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: t('settings.passwordRequired'), trigger: 'blur' },
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
        // 初始化加密密钥
        await initKeys()
        
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
        
        ElMessage.success(t('settings.passwordChangeSuccess'))
        
        localStorage.removeItem('auth_token')
        setTimeout(() => {
          router.push('/login')
        }, 1500)
      } catch (error) {
        console.error('Change password error:', error)
        ElMessage.error(error.response?.data?.message || t('common.error'))
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