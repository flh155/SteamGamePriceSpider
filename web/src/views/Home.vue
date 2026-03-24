<template>
  <div class="home">
    <!-- API Key 设置提示弹窗 -->
    <el-dialog
      v-model="showApiKeyDialog"
      :title="t('home.apiKeyConfig.title')"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      :show-close="false"
      width="500px"
      class="api-key-dialog"
    >
      <div class="dialog-content">
        <div class="warning-banner">
          <span class="warning-icon">⚠️</span>
          <p class="warning-text">{{ t('home.apiKeyConfig.warningText') }}</p>
        </div>
        
        <el-form
          ref="apiKeyFormRef"
          :model="apiKeyForm"
          :rules="apiKeyRules"
          label-position="top"
        >
          <el-form-item :label="t('home.apiKeyConfig.label')" prop="apiKey">
            <el-input
              v-model="apiKeyForm.apiKey"
              type="password"
              :placeholder="t('home.apiKeyConfig.placeholder')"
              show-password
              clearable
              size="large"
            />
            <div class="form-tip">
              ℹ️ {{ t('home.apiKeyConfig.tip1') }}<br>
              💡 <a href="https://isthereanydeal.com/apps/" target="_blank">{{ t('home.apiKeyConfig.tip2') }}</a>
            </div>
          </el-form-item>
        </el-form>
      </div>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button 
            type="primary" 
            :loading="savingApiKey" 
            @click="handleSaveApiKey"
            size="large"
          >
            {{ t('home.apiKeyConfig.saveAndContinue') }}
          </el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 搜索区域 -->
    <section class="search-section">
      <div class="search-container">
        <h1 class="search-title">{{ t('home.title') }}</h1>
        <p class="search-subtitle">{{ t('home.subtitle') }}</p>
        
        <div class="search-box">
          <el-input
            v-model="searchQuery"
            :placeholder="t('home.searchPlaceholder')"
            size="large"
            clearable
            @keyup.enter="handleSearch"
          >
            <template #prefix>
              <span class="search-icon">🔍</span>
            </template>
            <template #append>
              <el-button type="primary" @click="handleSearch" :loading="searching">
                {{ t('common.search') }}
              </el-button>
            </template>
          </el-input>
        </div>
      </div>
    </section>

    <!-- 错误提示 -->
    <section v-if="searchError" class="error-section">
      <div class="error-message">
        <span class="error-icon">⚠️</span>
        <span>{{ searchError }}</span>
        <el-button type="text" @click="searchError = null" size="small">
          {{ t('common.cancel') }}
        </el-button>
      </div>
    </section>

    <!-- 搜索结果 -->
    <section v-if="searchResult && !searchResult.data.error" class="result-section">
      <h2 class="section-title">{{ t('home.resultSection.title') }}</h2>
      <div class="price-card">
        <!-- 游戏封面图片 -->
        <div class="game-cover">
          <img 
            v-if="availableImageUrl" 
            :src="availableImageUrl" 
            :alt="searchResult.data.game_name"
            class="cover-image"
            @error="handleImageErrors"
          />
          <div v-else class="no-image">
            <span class="no-image-icon">🖼️</span>
            <p>{{ t('home.resultSection.noImage') }}</p>
          </div>
        </div>
        
        <div class="game-header">
          <h3 class="game-name">{{ searchResult.data.game_name }}</h3>
          <span class="game-id">#{{ searchResult.data.game_id }}</span>
        </div>
        
        <div class="price-grid">
          <div class="price-item highlight">
            <div class="price-label">{{ t('home.resultSection.currentLowestPrice') }}</div>
            <div class="price-value">¥{{ searchResult.data.best_price }}</div>
            <div class="price-shop">{{ t('home.resultSection.lowestShop') }}{{ searchResult.data.best_price_shop_name }}</div>
          </div>
          
          <div class="price-item">
            <div class="price-label">{{ t('home.resultSection.historicalLowestPrice') }}</div>
            <div class="price-value low">¥{{ searchResult.data.lowest_price }}</div>
            <div class="price-shop">{{ t('home.resultSection.lowestShopHistory') }}{{ searchResult.data.lowest_shop_name }}</div>
          </div>
          
          <div class="price-item">
            <div class="price-label">{{ t('home.resultSection.steamCurrentPrice') }}</div>
            <div class="price-value">¥{{ searchResult.data.now_steam_price }}</div>
            <div class="price-shop">{{ t('home.resultSection.steamShop') }}</div>
          </div>
        </div>
      </div>
    </section>
    
    <!-- 无数据状态 -->
    <section v-else-if="searchResult && searchResult.data.error" class="empty-result-section">
      <div class="empty-state">
        <span class="empty-icon">😔</span>
        <p>{{ searchResult.data.error }}</p>
      </div>
    </section>

    <!-- 热门游戏列表 - 暂时隐藏 -->
    <!-- <section class="hot-games-section">
      <div class="section-header">
        <h2 class="section-title">🔥 {{ t('common.hotGames') }}</h2>
        <el-button @click="loadHotGames" :loading="loadingHot" circle>
          <span>🔄</span>
        </el-button>
      </div>
      
      <div v-loading="loadingHot" class="games-grid">
        <div 
          v-for="game in hotGames" 
          :key="game.game_id"
          class="game-card"
        >
          <div class="card-header">
            <h3 class="card-game-name">{{ game.game_name }}</h3>
          </div>
          
          <div class="card-body">
            <div class="price-info">
              <span class="current-price">¥{{ game.best_price }}</span>
              <span class="currency">{{ game.currency }}</span>
            </div>
            <div class="shop-info">
              <span class="shop-name">{{ game.best_shop_name }}</span>
            </div>
          </div>
          
          <div class="card-footer">
            <el-button 
              size="small" 
              type="primary" 
              @click="viewGameDetail(game)"
              plain
            >
              {{ t('common.viewDetail') }}
            </el-button>
          </div>
        </div>
      </div>
      
      <div v-if="!loadingHot && hotGames.length === 0" class="empty-state">
        <p>{{ t('home.noData') }}</p>
      </div>
    </section> -->
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElLoading } from 'element-plus'
import { useI18n } from 'vue-i18n'
import { getGamePrice, getApiKey, setApiKey } from '../api/game'

const { t } = useI18n()

// API Key 相关
const showApiKeyDialog = ref(false)
const apiKeyFormRef = ref(null)
const savingApiKey = ref(false)
const hasApiKey = ref(false)

const apiKeyForm = reactive({
  apiKey: ''
})

const apiKeyRules = {
  apiKey: [
    { required: true, message: '请输入 API Key', trigger: 'blur' }
  ]
}

// 检查是否需要设置 API Key
const checkApiKeyStatus = async () => {
  try {
    const response = await getApiKey()
    console.log('Check API Key response:', response)
    
    // 检查响应是否成功且有数据
    if (response && response.code === 200 && response.data) {
      const apiKeyValue = response.data.api_key
      console.log('API Key value:', apiKeyValue)
      
      // 判断是否为空或空字符串
      if (!apiKeyValue || apiKeyValue.trim() === '') {
        hasApiKey.value = false
        showApiKeyDialog.value = true
        ElMessage.warning(t('home.apiKeyConfig.pleaseConfigApiKey'))
      } else {
        hasApiKey.value = true
      }
    } else {
      // 如果响应异常，也显示弹窗
      hasApiKey.value = false
      showApiKeyDialog.value = true
    }
  } catch (error) {
    console.error('Check API Key status error:', error)
    // 出错时也显示弹窗
    hasApiKey.value = false
    showApiKeyDialog.value = true
  }
}

// 保存 API Key
const handleSaveApiKey = async () => {
  if (!apiKeyFormRef.value) return
  
  await apiKeyFormRef.value.validate(async (valid) => {
    if (valid) {
      savingApiKey.value = true
      try {
        await setApiKey({
          api_key: apiKeyForm.apiKey
        })
        
        ElMessage.success(t('settings.saveApiKeySuccess'))
        showApiKeyDialog.value = false
        hasApiKey.value = true
      } catch (error) {
        console.error('Save API Key error:', error)
        ElMessage.error(error.response?.data?.message || t('common.error'))
      } finally {
        savingApiKey.value = false
      }
    }
  })
}

// 搜索相关
const searchQuery = ref('')
const searching = ref(false)
const searchResult = ref(null)
const searchError = ref(null)

// 获取可用的图片 URL（优先级：300x140 > 400x187 > 600x344 > 145x68 > boxart）
const availableImageUrl = computed(() => {
  if (!searchResult.value?.data?.pic_url) {
    return null
  }
  
  const picUrls = searchResult.value.data.pic_url
  const priorityKeys = ['300x140', '400x187', '600x344', '145x68', 'boxart']
  
  for (const key of priorityKeys) {
    if (picUrls[key]) {
      return picUrls[key]
    }
  }
  
  return null
})

// 图片加载错误处理
const handleImageErrors = (e) => {
  console.warn('图片加载失败:', e.target.src)
  e.target.style.display = 'none'
  const noImageDiv = e.target.nextElementSibling
  if (noImageDiv && noImageDiv.classList.contains('no-image')) {
    noImageDiv.style.display = 'flex'
  }
}

// 搜索处理
const handleSearch = async () => {
  if (!searchQuery.value.trim()) {
    ElMessage.warning(t('home.pleaseEnterGameName'))
    return
  }
  
  // 如果没有 API Key，禁止搜索并显示弹窗
  if (!hasApiKey.value) {
    ElMessage.warning(t('home.apiKeyConfig.pleaseConfigApiKey'))
    showApiKeyDialog.value = true
    return
  }
  
  searching.value = true
  searchError.value = null
  searchResult.value = null
  
  // 显示加载提示
  const loadingInstance = ElLoading.service({
    lock: true,
    text: t('home.searching'),
    background: 'rgba(0, 0, 0, 0.7)'
  })
  
  try {
    const response = await getGamePrice(searchQuery.value.trim())
    if (response.data && response.data.error) {
      searchError.value = response.data.error
    } else {
      searchResult.value = response
      ElMessage.success(t('home.searchSuccess'))
    }
  } catch (error) {
    console.error('Search error:', error)
    searchError.value = error.response?.data?.message || error.message || t('home.searchError')
    ElMessage.error(searchError.value)
  } finally {
    searching.value = false
    loadingInstance.close()
  }
}

// 加载热门游戏
const loadHotGames = async () => {
  loadingHot.value = true
  try {
    // TODO: 实现后端 API
    // const response = await getHotGames(20)
    // hotGames.value = response.data
    
    // 模拟数据用于演示
    hotGames.value = [
      {
        game_id: '1',
        game_name: 'Elden Ring',
        best_price: 198.00,
        best_shop_name: 'Steam',
        currency: 'CNY'
      },
      {
        game_id: '2',
        game_name: 'Cyberpunk 2077',
        best_price: 149.00,
        best_shop_name: 'GOG',
        currency: 'CNY'
      },
      {
        game_id: '3',
        game_name: 'Red Dead Redemption 2',
        best_price: 119.00,
        best_shop_name: 'Epic Game Store',
        currency: 'CNY'
      },
      {
        game_id: '4',
        game_name: 'The Witcher 3',
        best_price: 39.00,
        best_shop_name: 'Steam',
        currency: 'CNY'
      },
      {
        game_id: '5',
        game_name: 'God of War',
        best_price: 199.00,
        best_shop_name: 'Steam',
        currency: 'CNY'
      },
      {
        game_id: '6',
        game_name: 'Hades',
        best_price: 48.00,
        best_shop_name: 'Humble Store',
        currency: 'CNY'
      }
    ]
  } catch (error) {
    console.error('Load hot games error:', error)
    ElMessage.error(t('common.error'))
  } finally {
    loadingHot.value = false
  }
}

// 查看详情
const viewGameDetail = (game) => {
  searchQuery.value = game.game_name
  handleSearch()
}

onMounted(() => {
  checkApiKeyStatus()
  loadHotGames()
})
</script>

<style scoped>
.home {
  display: block;
  min-height: 100%;
}

/* API Key 弹窗样式 */
.dialog-content {
  padding: 0.5rem 0;
}

.warning-banner {
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.15) 0%, rgba(217, 119, 6, 0.15) 100%);
  border: 1px solid rgba(245, 158, 11, 0.3);
  border-radius: 8px;
  padding: 1rem 1.25rem;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.warning-icon {
  font-size: 1.5rem;
}

.warning-text {
  color: #fbbf24;
  font-weight: 500;
  margin: 0;
  font-size: 0.95rem;
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

:deep(.el-dialog__header) {
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid rgba(59, 130, 246, 0.2);
}

:deep(.el-dialog__title) {
  font-size: 1.3rem;
  font-weight: 600;
  color: #3b82f6;
}

:deep(.el-dialog__body) {
  padding: 1.5rem;
}

:deep(.el-dialog__footer) {
  padding: 1rem 1.5rem;
  border-top: 1px solid rgba(59, 130, 246, 0.2);
}

:deep(.el-input__wrapper) {
  background: rgba(15, 23, 42, 0.6);
  border-color: rgba(59, 130, 246, 0.3);
}

:deep(.el-input__inner) {
  color: #e0e7ff;
}

/* 搜索区域 */
.search-section {
  background: linear-gradient(135deg, #1e2a3a 0%, #252f40 100%);
  border-radius: 16px;
  padding: 3rem 2rem;
  text-align: center;
  border: 1px solid #2d3a4f;
  margin-bottom: 2rem;
}

.search-container {
  max-width: 800px;
  margin: 0 auto;
}

.search-title {
  font-size: 2.5rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  color: #3b82f6;
}

.search-subtitle {
  color: #9ca3af;
  font-size: 1.1rem;
  margin-bottom: 2rem;
}

.search-box {
  max-width: 600px;
  margin: 0 auto;
}

.search-icon {
  font-size: 1.2rem;
}

/* 错误提示 */
.error-section {
  margin-bottom: 2rem;
  animation: shakeIn 0.3s ease;
}

.error-message {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: 8px;
  padding: 1rem 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: #ef4444;
}

.error-icon {
  font-size: 1.5rem;
}

/* 搜索结果 */
.result-section {
  animation: fadeIn 0.3s ease;
  margin-bottom: 2rem;
}

.section-title {
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
  color: #e0e0e0;
}

.price-card {
  background: #252f40;
  border-radius: 12px;
  padding: 2rem;
  border: 1px solid #2d3a4f;
}

/* 游戏封面图片 */
.game-cover {
  width: 100%;
  max-width: 300px;
  margin: 0 auto 2rem auto;
  border-radius: 8px;
  overflow: hidden;
  background: #1e2a3a;
}

.cover-image {
  width: 100%;
  height: auto;
  display: block;
  object-fit: cover;
}

.no-image {
  width: 100%;
  height: 140px;
  display: none;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background: #1e2a3a;
  color: #6b7280;
}

.no-image-icon {
  font-size: 3rem;
  margin-bottom: 0.5rem;
  opacity: 0.5;
}

.no-image p {
  font-size: 0.9rem;
  margin: 0;
}

.game-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #2d3a4f;
}

.game-name {
  font-size: 1.5rem;
  color: #e0e0e0;
}

.game-id {
  color: #6b7280;
  font-size: 0.9rem;
}

.price-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
}

.price-item {
  background: #1e2a3a;
  padding: 1.5rem;
  border-radius: 8px;
  text-align: center;
  border: 1px solid #2d3a4f;
  transition: all 0.3s ease;
}

.price-item.highlight {
  border-color: #10b981;
  background: rgba(16, 185, 129, 0.1);
}

.price-label {
  color: #9ca3af;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.price-value {
  font-size: 2rem;
  font-weight: bold;
  color: #3b82f6;
  margin-bottom: 0.5rem;
}

.price-value.low {
  color: #10b981;
}

.price-shop {
  color: #6b7280;
  font-size: 0.9rem;
}

/* 空结果状态 */
.empty-result-section {
  margin-bottom: 2rem;
  animation: fadeIn 0.3s ease;
}

.empty-state {
  text-align: center;
  padding: 3rem;
  color: #6b7280;
  background: #252f40;
  border-radius: 12px;
  border: 1px solid #2d3a4f;
}

.empty-icon {
  font-size: 3rem;
  display: block;
  margin-bottom: 1rem;
}

/* 响应式 */
@media (max-width: 768px) {
  .search-title {
    font-size: 1.8rem;
  }
  
  .search-section {
    padding: 2rem 1rem;
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes shakeIn {
  0%, 100% {
    transform: translateX(0);
  }
  25% {
    transform: translateX(-5px);
  }
  75% {
    transform: translateX(5px);
  }
}
</style>