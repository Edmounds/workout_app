<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import AppLayout from './components/AppLayout.vue'

const router = useRouter()
const currentUser = ref(null)
const isDarkMode = ref(false)

// 检查用户登录状态
onMounted(() => {
  const userStr = localStorage.getItem('user')
  if (userStr) {
    try {
      currentUser.value = JSON.parse(userStr)
    } catch (e) {
      localStorage.removeItem('user')
      console.error('无法解析用户数据', e)
    }
  }
  
  // 检查暗色模式设置
  const darkModePreference = localStorage.getItem('darkMode')
  isDarkMode.value = darkModePreference === 'true'
})

// 切换暗色模式
const toggleDarkMode = () => {
  isDarkMode.value = !isDarkMode.value
  localStorage.setItem('darkMode', isDarkMode.value.toString())
}

// 注销用户
const logout = () => {
  localStorage.removeItem('user')
  currentUser.value = null
  router.push('/login')
}

// 检查是否在登录/注册页面
const isAuthPage = computed(() => {
  return router.currentRoute.value.path === '/login' || 
         router.currentRoute.value.path === '/register'
})
</script>

<template>
  <v-app :theme="isDarkMode ? 'dark' : 'light'">
    <!-- 使用AppLayout组件渲染已登录用户的布局 -->
    <AppLayout 
      v-if="currentUser && !isAuthPage" 
      :user="currentUser" 
      :isDarkMode="isDarkMode"
      @toggle-dark-mode="toggleDarkMode"
      @logout="logout"
    >
      <router-view></router-view>
    </AppLayout>
    
    <!-- 对于登录/注册页面，直接渲染 -->
    <v-main v-else>
      <router-view></router-view>
    </v-main>
  </v-app>
</template>

<style>
/* 全局样式 */
:root {
  --primary-color: #2196F3;
  --secondary-color: #03A9F4;
  --accent-color: #E91E63;
  --error-color: #FF5252;
  --success-color: #4CAF50;
  --warning-color: #FFC107;
  --info-color: #00BCD4;
}
</style>
