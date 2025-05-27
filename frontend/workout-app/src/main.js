import './assets/main.css'

import { createApp } from 'vue'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css'

import App from './App.vue'
import router from './router'

// 配置Vuetify
const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        colors: {
          primary: '#2196F3',
          secondary: '#03A9F4',
          accent: '#E91E63',
          error: '#FF5252',
          info: '#00BCD4',
          success: '#4CAF50',
          warning: '#FFC107',
          background: '#f5f5f5'
        }
      },
      dark: {
        colors: {
          primary: '#2196F3',
          secondary: '#03A9F4',
          accent: '#E91E63',
          error: '#FF5252',
          info: '#00BCD4',
          success: '#4CAF50',
          warning: '#FFC107',
          background: '#121212'
        }
      }
    }
  }
})

// 创建Vue应用实例
const app = createApp(App)

// 使用插件
app.use(router) // 注册路由
app.mount('#app') // 挂载应用
