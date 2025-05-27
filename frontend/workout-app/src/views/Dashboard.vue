<template>
  <v-container fluid>
    <!-- 数据概览头部 -->
    <v-row class="mb-4">
      <v-col cols="12">
        <h1 class="text-h4 font-weight-bold">数据概览</h1>
        <p class="text-subtitle-1 text-medium-emphasis">欢迎回来，{{ userName }}！这是您的健康运动数据概览。</p>
      </v-col>
    </v-row>

    <!-- 加载状态指示器 -->
    <v-progress-linear
      v-if="loading"
      indeterminate
      color="primary"
    ></v-progress-linear>

    <!-- 错误提示 -->
    <v-alert
      v-if="error"
      type="error"
      closable
      class="mb-4"
      @click:close="error = ''"
    >
      {{ error }}
    </v-alert>

    <!-- 数据卡片 -->
    <v-row>
      <v-col cols="12" sm="6" lg="3">
        <v-card class="mx-auto" height="150">
          <v-card-item>
            <v-card-title>总运动次数</v-card-title>
          </v-card-item>
          <v-card-text class="d-flex justify-center align-center">
            <span class="text-h3 font-weight-bold">{{ overallStats.workout_count || 0 }}</span>
            <span class="text-subtitle-1 ml-2">次</span>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" lg="3">
        <v-card class="mx-auto" height="150">
          <v-card-item>
            <v-card-title>总距离</v-card-title>
          </v-card-item>
          <v-card-text class="d-flex justify-center align-center">
            <span class="text-h3 font-weight-bold">{{ formatDistance(overallStats.total_distance) }}</span>
            <span class="text-subtitle-1 ml-2">公里</span>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" lg="3">
        <v-card class="mx-auto" height="150">
          <v-card-item>
            <v-card-title>总时长</v-card-title>
          </v-card-item>
          <v-card-text class="d-flex justify-center align-center">
            <span class="text-h3 font-weight-bold">{{ formatDuration(overallStats.total_duration) }}</span>
            <span class="text-subtitle-1 ml-2">小时</span>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" lg="3">
        <v-card class="mx-auto" height="150">
          <v-card-item>
            <v-card-title>消耗卡路里</v-card-title>
          </v-card-item>
          <v-card-text class="d-flex justify-center align-center">
            <span class="text-h3 font-weight-bold">{{ formatCalories(overallStats.total_calories) }}</span>
            <span class="text-subtitle-1 ml-2">千卡</span>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- 图表区域 -->
    <v-row class="mt-4">
      <v-col cols="12" lg="8">
        <v-card>
          <v-card-item>
            <v-card-title>本周运动趋势</v-card-title>
            <template v-slot:append>
              <v-btn-toggle v-model="chartDateRange" mandatory color="primary" density="comfortable">
                <v-btn value="week">周</v-btn>
                <v-btn value="month">月</v-btn>
                <v-btn value="year">年</v-btn>
              </v-btn-toggle>
            </template>
          </v-card-item>
          <v-card-text>
            <div style="height: 350px;">
              <line-chart :chart-data="workoutChartData" :options="chartOptions"></line-chart>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" lg="4">
        <v-card class="mb-4">
          <v-card-item>
            <v-card-title>运动类型分布</v-card-title>
          </v-card-item>
          <v-card-text>
            <div style="height: 250px;">
              <pie-chart :chart-data="workoutTypeChartData" :options="pieChartOptions"></pie-chart>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- 健康建议和目标完成情况 -->
    <v-row class="mt-4">
      <v-col cols="12" lg="6">
        <v-card>
          <v-card-item>
            <v-card-title>AI健康建议</v-card-title>
            <template v-slot:append>
              <v-btn size="small" color="primary" variant="text" @click="refreshAdvice">刷新</v-btn>
            </template>
          </v-card-item>
          <v-list lines="two">
            <v-list-item v-for="(advice, index) in aiAdvice" :key="index">
              <v-list-item-title class="font-weight-medium">{{ advice.category || '日常建议' }}</v-list-item-title>
              <v-list-item-subtitle>{{ advice.content }}</v-list-item-subtitle>
            </v-list-item>
            <v-list-item v-if="!aiAdvice.length">
              <v-list-item-title>暂无建议</v-list-item-title>
              <v-list-item-subtitle>更新您的运动数据以获取个性化建议</v-list-item-subtitle>
            </v-list-item>
          </v-list>
        </v-card>
      </v-col>

      <v-col cols="12" lg="6">
        <v-card>
          <v-card-item>
            <v-card-title>进度目标</v-card-title>
            <template v-slot:append>
              <v-btn size="small" color="primary" variant="text" @click="showAddGoalDialog = true">添加目标</v-btn>
            </template>
          </v-card-item>
          <v-list>
            <v-list-item v-for="(goal, index) in goals" :key="goal.id || index">
              <template v-slot:prepend>
                <v-avatar :color="goalColor(goal)" size="40">
                  <v-icon color="white">{{ goalIcon(goal) }}</v-icon>
                </v-avatar>
              </template>
              <v-list-item-title>{{ goal.title }}</v-list-item-title>
              <v-list-item-subtitle>
                <v-progress-linear
                  :model-value="goalProgress(goal)"
                  :color="goalColor(goal)"
                  height="8"
                  rounded
                  class="my-1"
                >
                  <template v-slot:default="{ value }">
                    <span class="text-caption">{{ Math.round(value) }}% 完成</span>
                  </template>
                </v-progress-linear>
                {{ goal.current_value }} / {{ goal.target_value }} {{ goal.category }}
              </v-list-item-subtitle>
            </v-list-item>
            <v-list-item v-if="!goals.length">
              <v-list-item-title>暂无目标</v-list-item-title>
              <v-list-item-subtitle>点击"添加目标"开始设定您的健康目标</v-list-item-subtitle>
            </v-list-item>
          </v-list>
        </v-card>
      </v-col>
    </v-row>

    <!-- 最近运动记录 -->
    <v-row class="mt-4">
      <v-col cols="12">
        <v-card>
          <v-card-item>
            <v-card-title>最近运动记录</v-card-title>
            <template v-slot:append>
              <v-btn size="small" color="primary" variant="text" @click="$router.push({name: 'UserStats'})">查看全部</v-btn>
            </template>
          </v-card-item>
          <v-table>
            <thead>
              <tr>
                <th>类型</th>
                <th>日期</th>
                <th>时长</th>
                <th>距离</th>
                <th>配速</th>
                <th>心率</th>
                <th>卡路里</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="record in recentRecords" :key="record.id">
                <td>{{ record.workout_type }}</td>
                <td>{{ formatDate(record.start_time) }}</td>
                <td>{{ formatDurationMinutes(record.duration) }}</td>
                <td>{{ formatDistance(record.distance) }} 公里</td>
                <td>{{ formatPace(record.avg_pace) }}</td>
                <td>{{ record.avg_heart_rate }} 次/分</td>
                <td>{{ record.calories }} 千卡</td>
              </tr>
              <tr v-if="!recentRecords.length">
                <td colspan="7" class="text-center">暂无运动记录</td>
              </tr>
            </tbody>
          </v-table>
        </v-card>
      </v-col>
    </v-row>

    <!-- 添加目标对话框 -->
    <v-dialog v-model="showAddGoalDialog" max-width="600px">
      <v-card>
        <v-card-title>添加新目标</v-card-title>
        <v-card-text>
          <v-form ref="goalForm" v-model="validGoalForm">
            <v-text-field
              v-model="newGoal.title"
              label="目标标题"
              :rules="[v => !!v || '请输入目标标题']"
            ></v-text-field>
            
            <v-select
              v-model="newGoal.category"
              :items="goalCategories"
              label="目标类别"
              :rules="[v => !!v || '请选择目标类别']"
            ></v-select>
            
            <v-row>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="newGoal.current_value"
                  type="number"
                  label="当前值"
                  :rules="[v => v >= 0 || '当前值不能为负数']"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="newGoal.target_value"
                  type="number"
                  label="目标值"
                  :rules="[v => !!v || '请输入目标值', v => Number(v) > 0 || '目标值必须大于0']"
                ></v-text-field>
              </v-col>
            </v-row>
            
            <v-text-field
              v-model="newGoal.deadline"
              type="date"
              label="截止日期"
            ></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey-darken-1" variant="text" @click="showAddGoalDialog = false">取消</v-btn>
          <v-btn color="primary" @click="addGoal" :loading="savingGoal">保存</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import { workoutService, healthService, adviceService, progressService } from '@/services/api';
import { Line as LineChart, Pie as PieChart } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, LinearScale, CategoryScale, PointElement, ArcElement } from 'chart.js';

// 注册 Chart.js 组件
ChartJS.register(Title, Tooltip, Legend, LineElement, LinearScale, CategoryScale, PointElement, ArcElement);

export default {
  name: 'Dashboard',
  components: {
    LineChart,
    PieChart
  },
  data() {
    return {
      loading: false,
      error: '',
      userId: null,
      overallStats: {
        workout_count: 0,
        total_duration: 0,
        total_distance: 0,
        total_calories: 0
      },
      workoutStats: [],
      recentRecords: [],
      aiAdvice: [],
      goals: [],
      chartDateRange: 'week',
      showAddGoalDialog: false,
      validGoalForm: false,
      savingGoal: false,
      newGoal: {
        title: '',
        category: '',
        current_value: 0,
        target_value: 0,
        deadline: new Date().toISOString().split('T')[0]
      },
      goalCategories: ['距离', '时间', '次数', '卡路里', '体重'],
    };
  },
  computed: {
    user() {
      try {
        return JSON.parse(localStorage.getItem('user')) || {};
      } catch (e) {
        return {};
      }
    },
    userName() {
      return this.user.username || '用户';
    },
    // 图表数据
    workoutChartData() {
      // 生成日期标签
      const labels = this.generateDateLabels();
      
      // 模拟或真实数据
      const distances = this.generateChartData(labels.length, 10, 3);
      const durations = this.generateChartData(labels.length, 60, 15);
      
      return {
        labels,
        datasets: [
          {
            label: '距离 (公里)',
            backgroundColor: 'rgba(25, 118, 210, 0.2)',
            borderColor: 'rgba(25, 118, 210, 1)',
            data: distances,
            yAxisID: 'y'
          },
          {
            label: '时间 (分钟)',
            backgroundColor: 'rgba(76, 175, 80, 0.2)',
            borderColor: 'rgba(76, 175, 80, 1)',
            data: durations,
            yAxisID: 'y1'
          }
        ]
      };
    },
    workoutTypeChartData() {
      // 从workoutStats生成类型分布数据
      const types = this.workoutStats.map(stat => stat.workout_type || '未知');
      const distances = this.workoutStats.map(stat => stat.total_distance || 0);
      
      // 如果没有数据，提供默认数据
      if (types.length === 0) {
        return {
          labels: ['跑步', '步行', '骑行', '其他'],
          datasets: [{
            backgroundColor: ['#1976D2', '#4CAF50', '#FF9800', '#9C27B0'],
            data: [5, 3, 2, 1]
          }]
        };
      }
      
      return {
        labels: types,
        datasets: [{
          backgroundColor: ['#1976D2', '#4CAF50', '#FF9800', '#9C27B0', '#E53935', '#00BCD4'],
          data: distances
        }]
      };
    },
    chartOptions() {
      return {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: {
            grid: {
              display: false
            }
          },
          y: {
            position: 'left',
            title: {
              display: true,
              text: '距离 (公里)'
            }
          },
          y1: {
            position: 'right',
            title: {
              display: true,
              text: '时间 (分钟)'
            },
            grid: {
              drawOnChartArea: false
            }
          }
        }
      };
    },
    pieChartOptions() {
      return {
        responsive: true,
        maintainAspectRatio: false
      };
    }
  },
  methods: {
    async loadData() {
      if (!this.user.id) {
        this.error = '用户信息不存在，请重新登录';
        return;
      }
      
      this.userId = this.user.id;
      this.loading = true;
      this.error = '';
      
      try {
        // 加载健康统计数据
        const healthResponse = await healthService.getHealthStats(this.userId);
        if (healthResponse.data && healthResponse.data.data) {
          const healthData = healthResponse.data.data;
          this.overallStats = healthData.overall_stats || this.overallStats;
          this.workoutStats = healthData.workout_stats || [];
        }
        
        // 加载最近运动记录
        const recordsResponse = await workoutService.getRunningRecords(this.userId);
        if (recordsResponse.data && recordsResponse.data.data) {
          this.recentRecords = recordsResponse.data.data.slice(0, 5); // 只显示最近5条
        }
        
        // 加载AI建议
        const adviceResponse = await adviceService.getAiAdvice(this.userId);
        if (adviceResponse.data && adviceResponse.data.data) {
          this.aiAdvice = adviceResponse.data.data.slice(0, 3); // 只显示3条建议
        }
        
        // 加载进度目标
        const goalsResponse = await progressService.getGoals(this.userId);
        if (goalsResponse.data && goalsResponse.data.data) {
          this.goals = goalsResponse.data.data.slice(0, 4); // 只显示4个目标
        }
      } catch (error) {
        console.error('数据加载失败:', error);
        this.error = '数据加载失败，请稍后再试';
      } finally {
        this.loading = false;
      }
    },
    refreshAdvice() {
      if (this.userId) {
        adviceService.getAiAdvice(this.userId)
          .then(response => {
            if (response.data && response.data.data) {
              this.aiAdvice = response.data.data.slice(0, 3);
            }
          })
          .catch(error => {
            console.error('刷新建议失败:', error);
          });
      }
    },
    async addGoal() {
      if (!this.$refs.goalForm.validate()) return;
      
      this.savingGoal = true;
      
      try {
        const goalData = {
          user_id: this.userId,
          title: this.newGoal.title,
          category: this.newGoal.category,
          current_value: parseFloat(this.newGoal.current_value) || 0,
          target_value: parseFloat(this.newGoal.target_value),
          deadline: this.newGoal.deadline || null
        };
        
        const response = await progressService.createGoal(goalData);
        
        if (response.data) {
          // 重新加载目标
          const goalsResponse = await progressService.getGoals(this.userId);
          if (goalsResponse.data && goalsResponse.data.data) {
            this.goals = goalsResponse.data.data.slice(0, 4);
          }
          
          // 关闭对话框并重置表单
          this.showAddGoalDialog = false;
          this.newGoal = {
            title: '',
            category: '',
            current_value: 0,
            target_value: 0,
            deadline: new Date().toISOString().split('T')[0]
          };
        }
      } catch (error) {
        console.error('添加目标失败:', error);
        this.error = '添加目标失败，请稍后再试';
      } finally {
        this.savingGoal = false;
      }
    },
    // 工具函数
    formatDistance(distance) {
      if (!distance) return '0';
      // 假设后端返回的是米，转换为公里
      return (distance / 1000).toFixed(2);
    },
    formatDuration(seconds) {
      if (!seconds) return '0';
      // 转换为小时
      return (seconds / 3600).toFixed(1);
    },
    formatDurationMinutes(seconds) {
      if (!seconds) return '0';
      const hours = Math.floor(seconds / 3600);
      const minutes = Math.floor((seconds % 3600) / 60);
      return hours > 0 ? `${hours}小时${minutes}分` : `${minutes}分`;
    },
    formatCalories(calories) {
      if (!calories) return '0';
      return calories.toLocaleString();
    },
    formatDate(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
    },
    formatPace(pace) {
      if (!pace) return '-';
      const minutes = Math.floor(pace / 60);
      const seconds = pace % 60;
      return `${minutes}'${String(seconds).padStart(2, '0')}"`;
    },
    goalProgress(goal) {
      if (!goal.target_value) return 0;
      const progress = (goal.current_value / goal.target_value) * 100;
      return Math.min(progress, 100); // 最多显示100%
    },
    goalColor(goal) {
      const progress = this.goalProgress(goal);
      if (progress >= 100) return 'success';
      if (progress >= 60) return 'info';
      if (progress >= 30) return 'warning';
      return 'error';
    },
    goalIcon(goal) {
      const category = goal.category;
      if (category === '距离') return 'mdi-map-marker-distance';
      if (category === '时间') return 'mdi-clock-outline';
      if (category === '次数') return 'mdi-counter';
      if (category === '卡路里') return 'mdi-fire';
      if (category === '体重') return 'mdi-scale-bathroom';
      return 'mdi-flag';
    },
    // 图表相关函数
    generateDateLabels() {
      const today = new Date();
      const labels = [];
      
      let days;
      switch (this.chartDateRange) {
        case 'week':
          days = 7;
          break;
        case 'month':
          days = 30;
          break;
        case 'year':
          // 年视图使用月份
          for (let i = 11; i >= 0; i--) {
            const month = new Date(today.getFullYear(), today.getMonth() - i, 1);
            const monthName = month.toLocaleString('default', { month: 'short' });
            labels.push(monthName);
          }
          return labels;
        default:
          days = 7;
      }
      
      for (let i = days - 1; i >= 0; i--) {
        const date = new Date(today);
        date.setDate(today.getDate() - i);
        const dayString = date.toLocaleDateString('default', { weekday: 'short', day: 'numeric' });
        labels.push(dayString);
      }
      
      return labels;
    },
    generateChartData(count, max, variation) {
      // 为图表生成模拟数据
      const data = [];
      for (let i = 0; i < count; i++) {
        data.push(Math.round((Math.random() * variation + max - variation / 2) * 10) / 10);
      }
      return data;
    }
  },
  created() {
    this.loadData();
  }
};
</script>
