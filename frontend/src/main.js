// frontend/src/main.js

import { createApp } from 'vue'

// 引入 Element Plus
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

// 引入我們自己的 Tailwind CSS
import './style.css'

import App from './App.vue'

const app = createApp(App)

// 全域註冊所有 Element Plus Icons
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.use(ElementPlus)
app.mount('#app')