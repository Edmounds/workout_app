import axios from 'axios';

// 创建axios实例
const apiClient = axios.create({
  baseURL: 'http://localhost:5000',
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000
});

// 请求拦截器：添加认证信息
apiClient.interceptors.request.use(
  config => {
    const user = JSON.parse(localStorage.getItem('user'));
    if (user && user.token) {
      config.headers.Authorization = `Bearer ${user.token}`;
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

// 响应拦截器：处理错误
apiClient.interceptors.response.use(
  response => {
    return response;
  },
  error => {
    // 处理401错误（未授权）
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// 用户相关API
const userService = {
  // 用户登录
  login(credentials) {
    return apiClient.post('/api/users/login', credentials);
  },
  
  // 用户注册
  register(userData) {
    return apiClient.post('/api/user/register', userData);
  },
  
  // 获取用户信息
  getUserProfile(userId) {
    return apiClient.get(`/api/users/profile?id=${userId}`);
  },
  
  // 更新用户信息
  updateUserProfile(userData) {
    return apiClient.put('/api/user/update', userData);
  }
};

// 运动数据相关API
const workoutService = {
  // 上传运动数据
  uploadWorkout(workoutData) {
    return apiClient.post('/api/workout/upload', workoutData);
  },
  
  // 获取运动记录列表
  getRunningRecords(userId, startDate = null, endDate = null) {
    let url = `/api/user/running_records?user_id=${userId}`;
    if (startDate) url += `&start_date=${startDate}`;
    if (endDate) url += `&end_date=${endDate}`;
    return apiClient.get(url);
  }
};

// 健康数据相关API
const healthService = {
  // 获取健康统计数据
  getHealthStats(userId, date = null) {
    let url = `/api/health/stats?user_id=${userId}`;
    if (date) url += `&date=${date}`;
    return apiClient.get(url);
  }
};

// 训练计划相关API
const progressService = {
  // 获取进度目标
  getGoals(userId) {
    return apiClient.get(`/api/progress/goals?user_id=${userId}`);
  },
  
  // 创建进度目标
  createGoal(goalData) {
    return apiClient.post('/api/progress/goals', goalData);
  },
  
  // 更新进度目标
  updateGoal(goalId, goalData) {
    return apiClient.put(`/api/progress/goals/${goalId}`, goalData);
  },
  
  // 删除进度目标
  deleteGoal(goalId) {
    return apiClient.delete(`/api/progress/goals/${goalId}`);
  }
};

// 营养与AI建议相关API
const adviceService = {
  // 获取营养提示
  getNutritionTips(category = null, importance = null) {
    let url = '/api/nutrition/tips';
    const params = [];
    if (category) params.push(`category=${category}`);
    if (importance) params.push(`importance=${importance}`);
    if (params.length > 0) url += `?${params.join('&')}`;
    return apiClient.get(url);
  },
  
  // 获取AI建议
  getAiAdvice(userId, category = null) {
    let url = `/api/ai/advice?user_id=${userId}`;
    if (category) url += `&category=${category}`;
    return apiClient.get(url);
  }
};

// AI Token相关API
const aiService = {
  // 获取用户的Deepseek API Token
  getDeepseekToken(userId) {
    return apiClient.get(`/api/ai/token?user_id=${userId}`);
  },
  
  // 保存用户的Deepseek API Token
  saveDeepseekToken(userId, tokenData) {
    return apiClient.post('/api/ai/token', { user_id: userId, ...tokenData });
  },
  
  // 删除用户的Deepseek API Token
  deleteDeepseekToken(userId) {
    return apiClient.delete(`/api/ai/token?user_id=${userId}`);
  },
  
  // 获取Token使用统计
  getTokenStats(userId) {
    return apiClient.get(`/api/ai/token/stats?user_id=${userId}`);
  }
};

// 用户反馈相关API
const feedbackService = {
  // 提交用户反馈
  submitFeedback(feedbackData) {
    return apiClient.post('/api/user/feedback', feedbackData);
  }
};

// 时间胶囊相关API
const timeCapsuleService = {
  // 创建时间胶囊
  createTimeCapsule(capsuleData) {
    return apiClient.post('/api/time_capsule', capsuleData);
  },
  
  // 获取时间胶囊
  getTimeCapsules(userId) {
    return apiClient.get(`/api/time_capsule?user_id=${userId}`);
  }
};

// 导出所有API服务
export {
  userService,
  workoutService,
  healthService,
  progressService,
  adviceService,
  aiService,
  feedbackService,
  timeCapsuleService
};
