import { createRouter, createWebHistory } from 'vue-router';

// 导入页面组件
import Dashboard from '@/views/Dashboard.vue';
import UserStats from '@/views/UserStats.vue';
import AiToken from '@/views/AiToken.vue';
import Login from '@/views/Login.vue';
import Register from '@/views/Register.vue';
import NotFound from '@/views/NotFound.vue';

// 路由配置
const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true, title: '数据概览' }
  },
  {
    path: '/user-stats',
    name: 'UserStats',
    component: UserStats,
    meta: { requiresAuth: true, title: '用户统计' }
  },
  {
    path: '/ai-token',
    name: 'AiToken',
    component: AiToken,
    meta: { requiresAuth: true, title: 'AI Token查询' }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresAuth: false, title: '登录' }
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: { requiresAuth: false, title: '注册' }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFound,
    meta: { requiresAuth: false, title: '页面未找到' }
  }
];

// 创建路由实例
const router = createRouter({
  history: createWebHistory(),
  routes
});

// 导航守卫：检查是否需要登录
router.beforeEach((to, from, next) => {
  // 更新页面标题
  document.title = `${to.meta.title || '运动手环'} - 健康运动管理系统`;
  
  // 判断是否需要登录认证
  const isAuthenticated = localStorage.getItem('user') !== null;
  
  if (to.meta.requiresAuth && !isAuthenticated) {
    // 需要认证但未认证，重定向到登录页
    next({ name: 'Login', query: { redirect: to.fullPath } });
  } else {
    // 继续正常导航
    next();
  }
});

export default router;
