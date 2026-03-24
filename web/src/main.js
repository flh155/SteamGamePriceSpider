import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import { initKeys } from './utils/crypto'

async function startApp() {
  try {
    await initKeys()
    console.log('加密密钥初始化完成')
    
    const app = createApp(App)
    app.use(router)
    app.use(ElementPlus)
    app.mount('#app')
  } catch (error) {
    console.error('应用启动失败:', error)
    alert('应用启动失败，请刷新页面重试')
  }
}

startApp()