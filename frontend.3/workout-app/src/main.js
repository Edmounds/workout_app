import './assets/main.css'

import { createApp } from 'vue'
import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css'

import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify' // 导入vuetify插件

// 创建Vue应用实例
const app = createApp(App)

// 使用插件
app.use(router) // 注册路由
app.use(vuetify) // 注册Vuetify
app.mount('#app') // 挂载应用
