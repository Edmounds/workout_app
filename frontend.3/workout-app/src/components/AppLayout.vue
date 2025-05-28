<template>
  <v-app>
    <!-- 顶部工具栏 -->
    <v-app-bar color="primary" dark>
      <v-app-bar-nav-icon v-if="isAuthenticated" @click="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title>健康运动管理系统</v-toolbar-title>
      <v-spacer></v-spacer>
      
      <!-- 搜索框 -->
      <v-text-field
        v-if="isAuthenticated"
        prepend-inner-icon="mdi-magnify"
        label="搜索..."
        variant="solo-filled"
        hide-details
        density="compact"
        class="hidden-sm-and-down"
        style="max-width: 300px;"
      ></v-text-field>
      
      <v-spacer></v-spacer>
      
      <!-- 暗黑模式切换 -->
      <v-btn icon @click="toggleTheme">
        <v-icon>{{ darkMode ? 'mdi-weather-sunny' : 'mdi-weather-night' }}</v-icon>
      </v-btn>
      
      <!-- 通知菜单 -->
      <v-menu v-if="isAuthenticated" location="bottom">
        <template v-slot:activator="{ props }">
          <v-btn icon v-bind="props">
            <v-badge :content="3" color="error">
              <v-icon>mdi-bell</v-icon>
            </v-badge>
          </v-btn>
        </template>
        <v-list>
          <v-list-item
            v-for="(notification, i) in notifications"
            :key="i"
            :value="notification"
          >
            <v-list-item-title>{{ notification.title }}</v-list-item-title>
            <v-list-item-subtitle>{{ notification.message }}</v-list-item-subtitle>
          </v-list-item>
        </v-list>
      </v-menu>
      
      <!-- 用户菜单 -->
      <v-menu v-if="isAuthenticated" location="bottom">
        <template v-slot:activator="{ props }">
          <v-btn icon v-bind="props">
            <v-avatar color="indigo" size="36">
              <span class="text-h6 white--text">{{ userInitials }}</span>
            </v-avatar>
          </v-btn>
        </template>
        <v-list>
          <v-list-item prepend-icon="mdi-account" title="个人资料" @click="goToProfile"></v-list-item>
          <v-list-item prepend-icon="mdi-cog" title="设置" @click="goToSettings"></v-list-item>
          <v-divider></v-divider>
          <v-list-item prepend-icon="mdi-logout" title="退出登录" @click="logout"></v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>

    <!-- 侧边导航 -->
    <v-navigation-drawer 
      v-if="isAuthenticated" 
      v-model="drawer" 
      :color="darkMode ? 'grey-darken-4' : 'grey-lighten-4'"
    >
      <v-list-item class="pa-4 text-center">
        <v-avatar color="primary" size="64" class="mb-2">
          <span class="text-h4 white--text">{{ userInitials }}</span>
        </v-avatar>
        <v-list-item-title class="text-h6">{{ userName }}</v-list-item-title>
        <v-list-item-subtitle>{{ userEmail }}</v-list-item-subtitle>
      </v-list-item>

      <v-divider></v-divider>

      <v-list :lines="false">
        <v-list-item
          v-for="item in menuItems"
          :key="item.title"
          :value="item"
          :to="item.to"
          :prepend-icon="item.icon"
          class="my-1"
        >
          <v-list-item-title>{{ item.title }}</v-list-item-title>
        </v-list-item>
      </v-list>
      
      <template v-slot:append>
        <div class="pa-3">
          <v-btn
            variant="outlined"
            color="primary"
            block
            prepend-icon="mdi-logout"
            @click="logout"
          >
            退出登录
          </v-btn>
        </div>
      </template>
    </v-navigation-drawer>

    <!-- 主内容区域 -->
    <v-main>
      <router-view></router-view>
    </v-main>
    
    <!-- 底部导航 -->
    <v-bottom-navigation
      v-if="isAuthenticated && isMobile"
      color="primary"
      grow
      :elevation="4"
    >
      <v-btn v-for="item in mobileMenuItems" :key="item.title" :to="item.to">
        <v-icon>{{ item.icon }}</v-icon>
        <span>{{ item.title }}</span>
      </v-btn>
    </v-bottom-navigation>
    
    <!-- 底部版权栏 -->
    <v-footer v-if="!isMobile" :color="darkMode ? 'grey-darken-4' : 'grey-lighten-4'" class="text-center d-flex flex-column">
      <div>
        <span>&copy; {{ new Date().getFullYear() }} — </span>
        <strong>健康运动管理系统</strong>
      </div>
    </v-footer>
  </v-app>
</template>

<script>
export default {
  name: 'AppLayout',
  // 定义接收的属性
  props: {
    user: {
      type: Object,
      default: () => ({})
    },
    isDarkMode: {
      type: Boolean,
      default: false
    }
  },
  // 定义组件事件
  emits: ['toggle-dark-mode', 'logout'],
  data() {
    return {
      drawer: true,
      windowWidth: window.innerWidth,
      menuItems: [
        { title: '数据概览', icon: 'mdi-view-dashboard', to: { name: 'Dashboard' } },
        { title: '用户统计', icon: 'mdi-account-group', to: { name: 'UserStats' } },
        { title: 'AI Token查询', icon: 'mdi-robot', to: { name: 'AiToken' } },
      ],
      mobileMenuItems: [
        { title: '概览', icon: 'mdi-view-dashboard', to: { name: 'Dashboard' } },
        { title: '统计', icon: 'mdi-account-group', to: { name: 'UserStats' } },
        { title: 'AI', icon: 'mdi-robot', to: { name: 'AiToken' } },
      ],
      notifications: [
        { title: '完成目标', message: '恭喜！您已完成本周跑步目标！' },
        { title: '新建议', message: 'AI为您生成了新的训练建议' },
        { title: '系统更新', message: '系统已更新到最新版本' },
      ],
    };
  },
  computed: {
    isAuthenticated() {
      return this.user && Object.keys(this.user).length > 0;
    },
    darkMode() {
      return this.isDarkMode;
    },
    userName() {
      return this.user?.username || '用户';
    },
    userEmail() {
      return this.user?.email || '';
    },
    userInitials() {
      const name = this.userName;
      if (!name) return '?';
      return name.charAt(0).toUpperCase();
    },
    isMobile() {
      // 使用储存的窗口宽度检测移动设备
      return this.windowWidth < 768;
    }
  },
  mounted() {
    // 添加窗口大小监听
    window.addEventListener('resize', this.handleResize);
  },
  beforeUnmount() {
    // 移除窗口大小监听
    window.removeEventListener('resize', this.handleResize);
  },
  methods: {
    handleResize() {
      this.windowWidth = window.innerWidth;
    },
    toggleTheme() {
      // 发送事件到父组件处理
      this.$emit('toggle-dark-mode');
    },
    goToProfile() {
      // 跳转到个人资料页
      console.log('前往个人资料页');
    },
    goToSettings() {
      // 跳转到设置页
      console.log('前往设置页');
    },
    logout() {
      // 发送注销事件到父组件处理
      this.$emit('logout');
    }
  }
};
</script>
