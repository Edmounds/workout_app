<template>
  <v-container fluid>
    <!-- 用户统计头部 -->
    <v-row class="mb-4">
      <v-col cols="12">
        <h1 class="text-h4 font-weight-bold">用户统计</h1>
        <p class="text-subtitle-1 text-medium-emphasis">查看您的详细健康数据和统计信息</p>
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

    <!-- 日期选择器 -->
    <v-row>
      <v-col cols="12" md="6" lg="4">
        <v-card class="mb-4">
          <v-card-text>
            <v-row>
              <v-col cols="12">
                <v-menu
                  v-model="dateMenu"
                  :close-on-content-click="false"
                  min-width="auto"
                >
                  <template v-slot:activator="{ props }">
                    <v-text-field
                      v-model="selectedDate"
                      label="选择日期"
                      prepend-inner-icon="mdi-calendar"
                      readonly
                      v-bind="props"
                      variant="outlined"
                      density="comfortable"
                    ></v-text-field>
                  </template>
                  <v-date-picker
                    v-model="selectedDate"
                    @update:model-value="dateMenu = false"
                  ></v-date-picker>
                </v-menu>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- 健康数据卡片 -->
    <v-row>
      <v-col cols="12" sm="6" lg="3">
        <v-card class="mx-auto" height="150">
          <v-card-item>
            <v-card-title>步数</v-card-title>
          </v-card-item>
          <v-card-text class="d-flex justify-center align-center">
            <span class="text-h3 font-weight-bold">{{ healthStats.steps || 0 }}</span>
            <span class="text-subtitle-1 ml-2">步</span>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" lg="3">
        <v-card class="mx-auto" height="150">
          <v-card-item>
            <v-card-title>心率</v-card-title>
          </v-card-item>
          <v-card-text class="d-flex justify-center align-center">
            <span class="text-h3 font-weight-bold">{{ healthStats.heart_rate || 0 }}</span>
            <span class="text-subtitle-1 ml-2">bpm</span>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" lg="3">
        <v-card class="mx-auto" height="150">
          <v-card-item>
            <v-card-title>睡眠时长</v-card-title>
          </v-card-item>
          <v-card-text class="d-flex justify-center align-center">
            <span class="text-h3 font-weight-bold">{{ formatSleep(healthStats.sleep_duration) }}</span>
            <span class="text-subtitle-1 ml-2">小时</span>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" lg="3">
        <v-card class="mx-auto" height="150">
          <v-card-item>
            <v-card-title>卡路里消耗</v-card-title>
          </v-card-item>
          <v-card-text class="d-flex justify-center align-center">
            <span class="text-h3 font-weight-bold">{{ healthStats.calories_burned || 0 }}</span>
            <span class="text-subtitle-1 ml-2">千卡</span>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- 健康数据图表 -->
    <v-row class="mt-4">
      <v-col cols="12" md="6">
        <v-card>
          <v-card-item>
            <v-card-title>心率变化</v-card-title>
            <template v-slot:append>
              <v-btn-toggle v-model="heartRateRange" mandatory color="primary" density="comfortable">
                <v-btn value="day">日</v-btn>
                <v-btn value="week">周</v-btn>
                <v-btn value="month">月</v-btn>
              </v-btn-toggle>
            </template>
          </v-card-item>
          <v-card-text>
            <div style="height: 300px;">
              <line-chart :chart-data="heartRateChartData" :options="heartRateChartOptions"></line-chart>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="6">
        <v-card>
          <v-card-item>
            <v-card-title>睡眠质量</v-card-title>
            <template v-slot:append>
              <v-btn-toggle v-model="sleepQualityRange" mandatory color="primary" density="comfortable">
                <v-btn value="week">周</v-btn>
                <v-btn value="month">月</v-btn>
              </v-btn-toggle>
            </template>
          </v-card-item>
          <v-card-text>
            <div style="height: 300px;">
              <bar-chart :chart-data="sleepChartData" :options="sleepChartOptions"></bar-chart>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- 运动记录表格 -->
    <v-row class="mt-4">
      <v-col cols="12">
        <v-card>
          <v-card-item>
            <v-card-title>运动记录</v-card-title>
          </v-card-item>
          <v-card-text>
            <v-data-table
              :headers="headers"
              :items="workoutRecords"
              :items-per-page="5"
              class="elevation-1"
              hover
            >
              <template v-slot:item.date="{ item }">
                {{ formatDate(item.date) }}
              </template>
              <template v-slot:item.duration="{ item }">
                {{ formatDurationMin(item.duration) }}分钟
              </template>
              <template v-slot:item.distance="{ item }">
                {{ (item.distance / 1000).toFixed(2) }}公里
              </template>
              <template v-slot:item.calories="{ item }">
                {{ item.calories }}千卡
              </template>
              <template v-slot:item.actions="{ item }">
                <v-icon small class="mr-2" @click="viewWorkoutDetails(item)">
                  mdi-eye
                </v-icon>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- 目标进度 -->
    <v-row class="mt-4">
      <v-col cols="12">
        <v-card>
          <v-card-item>
            <v-card-title>目标进度</v-card-title>
            <template v-slot:append>
              <v-btn color="primary" prepend-icon="mdi-plus" @click="showGoalDialog = true">
                添加目标
              </v-btn>
            </template>
          </v-card-item>
          <v-card-text>
            <v-list v-if="goals.length > 0">
              <v-list-item v-for="(goal, index) in goals" :key="index" :value="goal">
                <template v-slot:prepend>
                  <v-avatar color="primary" :size="36" class="mr-3">
                    <v-icon>{{ getGoalIcon(goal.category) }}</v-icon>
                  </v-avatar>
                </template>
                <v-list-item-title>{{ goal.title }}</v-list-item-title>
                <v-list-item-subtitle>{{ goal.description }}</v-list-item-subtitle>
                <template v-slot:append>
                  <v-progress-linear
                    :model-value="goal.progress"
                    bg-color="grey-lighten-2"
                    color="primary"
                    height="20"
                    rounded
                    class="mt-2"
                  >
                    <template v-slot:default="{ value }">
                      <span class="font-weight-bold">{{ Math.round(value) }}%</span>
                    </template>
                  </v-progress-linear>
                </template>
              </v-list-item>
            </v-list>
            <p v-else class="text-center my-4">尚未设置目标，点击添加按钮创建新目标</p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- 添加目标对话框 -->
    <v-dialog v-model="showGoalDialog" max-width="500">
      <v-card>
        <v-card-title>添加新目标</v-card-title>
        <v-card-text>
          <v-form @submit.prevent="saveGoal" ref="goalForm">
            <v-text-field
              v-model="newGoal.title"
              label="目标名称"
              :rules="[v => !!v || '目标名称不能为空']"
              required
            ></v-text-field>
            <v-textarea
              v-model="newGoal.description"
              label="目标描述"
              rows="3"
            ></v-textarea>
            <v-select
              v-model="newGoal.category"
              :items="goalCategories"
              label="目标类型"
              :rules="[v => !!v || '请选择目标类型']"
              required
            ></v-select>
            <v-text-field
              v-model.number="newGoal.target_value"
              label="目标值"
              type="number"
              :rules="[v => !!v || '请输入目标值', v => v > 0 || '目标值必须大于0']"
              required
            ></v-text-field>
            <v-menu
              v-model="goalDateMenu"
              :close-on-content-click="false"
              min-width="auto"
            >
              <template v-slot:activator="{ props }">
                <v-text-field
                  v-model="newGoal.target_date"
                  label="目标日期"
                  prepend-inner-icon="mdi-calendar"
                  readonly
                  v-bind="props"
                  :rules="[v => !!v || '请选择目标日期']"
                  required
                ></v-text-field>
              </template>
              <v-date-picker
                v-model="newGoal.target_date"
                @update:model-value="goalDateMenu = false"
              ></v-date-picker>
            </v-menu>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey" text @click="showGoalDialog = false">取消</v-btn>
          <v-btn color="primary" @click="saveGoal">保存</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import { ref, reactive, computed, onMounted, watch } from 'vue';
import { healthService, workoutService, progressService } from '@/services/api';
import { format } from 'date-fns';
import LineChart from 'vue-chartjs';
import BarChart from 'vue-chartjs';

export default {
  name: 'UserStats',
  components: {
    LineChart,
    BarChart
  },
  setup() {
    const loading = ref(false);
    const error = ref('');
    const selectedDate = ref(format(new Date(), 'yyyy-MM-dd'));
    const dateMenu = ref(false);
    const healthStats = reactive({
      steps: 0,
      heart_rate: 0,
      sleep_duration: 0,
      calories_burned: 0,
    });
    const heartRateRange = ref('day');
    const sleepQualityRange = ref('week');
    const workoutRecords = ref([]);
    const goals = ref([]);
    const showGoalDialog = ref(false);
    const goalDateMenu = ref(false);
    const goalForm = ref(null);
    const newGoal = reactive({
      title: '',
      description: '',
      category: '',
      target_value: null,
      target_date: format(new Date(Date.now() + 30*24*60*60*1000), 'yyyy-MM-dd'), // 默认一个月后
    });

    const goalCategories = [
      { title: '步数目标', value: 'steps' },
      { title: '距离目标', value: 'distance' },
      { title: '运动次数', value: 'workouts' },
      { title: '卡路里消耗', value: 'calories' },
      { title: '睡眠质量', value: 'sleep' }
    ];

    const headers = [
      { title: '日期', key: 'date', align: 'start', sortable: true },
      { title: '类型', key: 'type', align: 'center' },
      { title: '时长', key: 'duration', align: 'end' },
      { title: '距离', key: 'distance', align: 'end' },
      { title: '卡路里', key: 'calories', align: 'end' },
      { title: '操作', key: 'actions', align: 'center', sortable: false }
    ];

    const heartRateChartData = computed(() => {
      // 根据选择的时间范围生成心率数据
      const labels = [];
      const data = [];
      
      if (heartRateRange.value === 'day') {
        // 生成一天内的小时数据
        for (let i = 0; i < 24; i += 2) {
          labels.push(`${i}:00`);
          data.push(Math.floor(Math.random() * 30) + 60); // 模拟数据
        }
      } else if (heartRateRange.value === 'week') {
        // 生成一周的日期
        const days = ['周一', '周二', '周三', '周四', '周五', '周六', '周日'];
        days.forEach(day => {
          labels.push(day);
          data.push(Math.floor(Math.random() * 20) + 65); // 模拟数据
        });
      } else {
        // 生成一个月的数据
        for (let i = 1; i <= 30; i += 3) {
          labels.push(`${i}日`);
          data.push(Math.floor(Math.random() * 25) + 60); // 模拟数据
        }
      }
      
      return {
        labels,
        datasets: [
          {
            label: '平均心率',
            data,
            borderColor: '#E53935',
            backgroundColor: 'rgba(229, 57, 53, 0.1)',
            borderWidth: 2,
            fill: true,
            tension: 0.4
          }
        ]
      };
    });

    const heartRateChartOptions = {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: false,
          min: 50,
          max: 120,
          title: {
            display: true,
            text: '心率 (bpm)'
          }
        }
      },
      plugins: {
        legend: {
          display: true
        },
        tooltip: {
          mode: 'index',
          intersect: false
        }
      }
    };

    const sleepChartData = computed(() => {
      // 生成睡眠数据
      const labels = [];
      const deepSleep = [];
      const lightSleep = [];
      
      if (sleepQualityRange.value === 'week') {
        // 生成一周的日期
        const days = ['周一', '周二', '周三', '周四', '周五', '周六', '周日'];
        days.forEach(day => {
          labels.push(day);
          deepSleep.push(Math.floor(Math.random() * 3) + 1); // 模拟深度睡眠
          lightSleep.push(Math.floor(Math.random() * 4) + 4); // 模拟浅度睡眠
        });
      } else {
        // 生成一个月的数据
        for (let i = 1; i <= 30; i += 3) {
          labels.push(`${i}日`);
          deepSleep.push(Math.floor(Math.random() * 3) + 1);
          lightSleep.push(Math.floor(Math.random() * 4) + 4);
        }
      }
      
      return {
        labels,
        datasets: [
          {
            label: '深度睡眠',
            data: deepSleep,
            backgroundColor: '#3949AB',
            borderColor: '#3949AB',
            borderWidth: 1
          },
          {
            label: '浅度睡眠',
            data: lightSleep,
            backgroundColor: '#90CAF9',
            borderColor: '#90CAF9',
            borderWidth: 1
          }
        ]
      };
    });

    const sleepChartOptions = {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          stacked: true
        },
        y: {
          stacked: true,
          title: {
            display: true,
            text: '小时'
          }
        }
      },
      plugins: {
        legend: {
          display: true
        }
      }
    };

    // 格式化函数
    const formatDate = (dateString) => {
      if (!dateString) return '';
      const date = new Date(dateString);
      return format(date, 'yyyy-MM-dd');
    };

    const formatSleep = (minutes) => {
      if (!minutes) return '0';
      return (minutes / 60).toFixed(1);
    };

    const formatDurationMin = (seconds) => {
      if (!seconds) return '0';
      return Math.round(seconds / 60);
    };

    const getGoalIcon = (category) => {
      const icons = {
        'steps': 'mdi-shoe-print',
        'distance': 'mdi-map-marker-distance',
        'workouts': 'mdi-weight-lifter',
        'calories': 'mdi-fire',
        'sleep': 'mdi-sleep'
      };
      return icons[category] || 'mdi-target';
    };

    // 获取健康统计数据
    const fetchHealthStats = async () => {
      try {
        loading.value = true;
        error.value = '';
        
        const userId = JSON.parse(localStorage.getItem('user')).id;
        const response = await healthService.getHealthStats(userId, selectedDate.value);
        
        if (response && response.data && response.data.data) {
          Object.assign(healthStats, response.data.data);
        }
      } catch (err) {
        console.error('获取健康数据失败:', err);
        error.value = '获取健康数据失败，请稍后再试';
      } finally {
        loading.value = false;
      }
    };

    // 获取运动记录
    const fetchWorkoutRecords = async () => {
      try {
        loading.value = true;
        error.value = '';
        
        const userId = JSON.parse(localStorage.getItem('user')).id;
        // 获取最近30天的运动记录
        const endDate = new Date();
        const startDate = new Date();
        startDate.setDate(endDate.getDate() - 30);
        
        const formattedStartDate = format(startDate, 'yyyy-MM-dd');
        const formattedEndDate = format(endDate, 'yyyy-MM-dd');
        
        const response = await workoutService.getRunningRecords(
          userId, formattedStartDate, formattedEndDate
        );
        
        if (response && response.data && response.data.data) {
          workoutRecords.value = response.data.data;
        }
      } catch (err) {
        console.error('获取运动记录失败:', err);
        error.value = '获取运动记录失败，请稍后再试';
      } finally {
        loading.value = false;
      }
    };

    // 获取目标数据
    const fetchGoals = async () => {
      try {
        loading.value = true;
        error.value = '';
        
        const userId = JSON.parse(localStorage.getItem('user')).id;
        const response = await progressService.getGoals(userId);
        
        if (response && response.data && response.data.data) {
          goals.value = response.data.data.map(goal => ({
            ...goal,
            progress: calculateProgress(goal)
          }));
        }
      } catch (err) {
        console.error('获取目标数据失败:', err);
        error.value = '获取目标数据失败，请稍后再试';
      } finally {
        loading.value = false;
      }
    };

    // 计算目标完成进度
    const calculateProgress = (goal) => {
      // 这里需要根据实际的目标类型和值来计算进度
      // 简化处理，随机生成进度
      return Math.floor(Math.random() * 100);
    };

    // 保存新目标
    const saveGoal = async () => {
      if (!goalForm.value.validate()) return;
      
      try {
        loading.value = true;
        error.value = '';
        
        const userId = JSON.parse(localStorage.getItem('user')).id;
        const goalData = {
          user_id: userId,
          title: newGoal.title,
          description: newGoal.description,
          category: newGoal.category,
          target_value: newGoal.target_value,
          target_date: newGoal.target_date
        };
        
        const response = await progressService.createGoal(goalData);
        
        if (response && response.data && response.data.data) {
          // 添加新创建的目标到列表中
          const createdGoal = response.data.data;
          goals.value.push({
            ...createdGoal,
            progress: 0 // 新目标进度为0
          });
          
          // 重置表单
          Object.assign(newGoal, {
            title: '',
            description: '',
            category: '',
            target_value: null,
            target_date: format(new Date(Date.now() + 30*24*60*60*1000), 'yyyy-MM-dd'),
          });
          
          showGoalDialog.value = false;
        }
      } catch (err) {
        console.error('保存目标失败:', err);
        error.value = '保存目标失败，请稍后再试';
      } finally {
        loading.value = false;
      }
    };

    // 查看运动详情
    const viewWorkoutDetails = (item) => {
      console.log('查看运动详情:', item);
      // 实现查看详情功能，可以弹窗显示
    };

    // 监听日期变化，更新健康数据
    watch(selectedDate, () => {
      fetchHealthStats();
    });

    // 页面加载时获取数据
    onMounted(() => {
      fetchHealthStats();
      fetchWorkoutRecords();
      fetchGoals();
    });

    return {
      loading,
      error,
      selectedDate,
      dateMenu,
      healthStats,
      heartRateRange,
      sleepQualityRange,
      heartRateChartData,
      heartRateChartOptions,
      sleepChartData,
      sleepChartOptions,
      workoutRecords,
      headers,
      goals,
      showGoalDialog,
      goalDateMenu,
      goalForm,
      newGoal,
      goalCategories,
      formatDate,
      formatSleep,
      formatDurationMin,
      getGoalIcon,
      viewWorkoutDetails,
      saveGoal
    };
  }
};
</script>

<style scoped>
.v-data-table {
  border-radius: 8px;
  overflow: hidden;
}
</style>
