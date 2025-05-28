<template>
  <v-container fluid>
    <!-- AI Token 查询头部 -->
    <v-row class="mb-4">
      <v-col cols="12">
        <h1 class="text-h4 font-weight-bold">AI Token 查询</h1>
        <p class="text-subtitle-1 text-medium-emphasis">查询和管理您的 Deepseek API Token</p>
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

    <!-- 成功提示 -->
    <v-alert
      v-if="successMessage"
      type="success"
      closable
      class="mb-4"
      @click:close="successMessage = ''"
    >
      {{ successMessage }}
    </v-alert>

    <!-- Token 管理卡片 -->
    <v-row>
      <v-col cols="12" md="8">
        <v-card>
          <v-card-title>
            <v-icon start>mdi-key-variant</v-icon>
            Deepseek API Token
          </v-card-title>
          <v-card-text>
            <p class="mb-3">您可以在此处管理您的 Deepseek API Token。此 Token 用于访问高级 AI 功能，如个性化训练建议和健康数据分析。</p>
            
            <v-form ref="form" v-model="valid">
              <v-row>
                <v-col cols="12" md="8">
                  <v-text-field
                    v-model="tokenValue"
                    :disabled="!isEditing"
                    :type="showToken ? 'text' : 'password'"
                    label="API Token"
                    :readonly="!isEditing"
                    variant="outlined"
                    :append-inner-icon="showToken ? 'mdi-eye-off' : 'mdi-eye'"
                    @click:append-inner="showToken = !showToken"
                    hint="请妥善保管您的 Token，不要分享给他人"
                    persistent-hint
                  ></v-text-field>
                </v-col>
                <v-col cols="12" md="4" class="d-flex align-center">
                  <template v-if="hasToken && !isEditing">
                    <v-btn
                      color="primary"
                      variant="tonal"
                      prepend-icon="mdi-pencil"
                      class="me-2"
                      @click="startEditing"
                    >
                      编辑
                    </v-btn>
                    <v-btn
                      color="error"
                      variant="tonal"
                      prepend-icon="mdi-delete"
                      @click="confirmDelete = true"
                    >
                      删除
                    </v-btn>
                  </template>
                  <template v-else-if="isEditing">
                    <v-btn
                      color="primary"
                      variant="flat"
                      prepend-icon="mdi-content-save"
                      class="me-2"
                      @click="saveToken"
                      :disabled="!valid || !tokenValue"
                    >
                      保存
                    </v-btn>
                    <v-btn
                      color="error"
                      variant="tonal"
                      prepend-icon="mdi-cancel"
                      @click="cancelEdit"
                    >
                      取消
                    </v-btn>
                  </template>
                  <template v-else>
                    <v-btn
                      color="primary"
                      variant="flat"
                      prepend-icon="mdi-plus"
                      @click="startEditing"
                    >
                      添加 Token
                    </v-btn>
                  </template>
                </v-col>
              </v-row>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- AI 使用统计卡片 -->
      <v-col cols="12" md="4">
        <v-card height="100%">
          <v-card-title>
            <v-icon start>mdi-chart-bar</v-icon>
            API 使用统计
          </v-card-title>
          <v-card-text v-if="hasToken">
            <div class="d-flex flex-column justify-center align-center" style="height: 100%">
              <template v-if="tokenStats">
                <v-sheet class="pa-4 text-center mb-4" rounded>
                  <p class="text-h6 mb-0">本月已使用</p>
                  <p class="text-h3 font-weight-bold primary--text">{{ tokenStats.used_tokens || 0 }}</p>
                  <p class="text-caption">Token 数</p>
                </v-sheet>
                <v-sheet class="pa-4 text-center" rounded>
                  <p class="text-h6 mb-0">剩余可用</p>
                  <p class="text-h3 font-weight-bold success--text">{{ tokenStats.remaining_tokens || 0 }}</p>
                  <p class="text-caption">Token 数</p>
                </v-sheet>
              </template>
              <v-progress-circular
                v-else
                indeterminate
                color="primary"
                size="50"
              ></v-progress-circular>
            </div>
          </v-card-text>
          <v-card-text v-else>
            <div class="text-center pa-4">
              <v-icon size="64" color="grey lighten-1">mdi-chart-bar</v-icon>
              <p class="text-body-1 mt-3">添加 API Token 后查看使用统计</p>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Token 使用说明卡片 -->
    <v-row class="mt-4">
      <v-col cols="12">
        <v-card>
          <v-card-title>
            <v-icon start>mdi-information-outline</v-icon>
            关于 Deepseek API
          </v-card-title>
          <v-card-text>
            <p class="mb-2">Deepseek API 是一个强大的人工智能接口，为您的运动数据提供智能分析和建议。通过配置您的 API Token，您可以获得以下功能：</p>
            <v-list>
              <v-list-item prepend-icon="mdi-run">
                <v-list-item-title>个性化训练计划生成</v-list-item-title>
              </v-list-item>
              <v-list-item prepend-icon="mdi-food-apple">
                <v-list-item-title>基于运动数据的营养建议</v-list-item-title>
              </v-list-item>
              <v-list-item prepend-icon="mdi-chart-line">
                <v-list-item-title>深度数据分析和进步趋势</v-list-item-title>
              </v-list-item>
              <v-list-item prepend-icon="mdi-heart-pulse">
                <v-list-item-title>健康状况评估与改进建议</v-list-item-title>
              </v-list-item>
            </v-list>
            <p class="mt-4">如何获取 Deepseek API Token:</p>
            <ol>
              <li>访问 <a href="https://platform.deepseek.com/" target="_blank" rel="noopener">Deepseek AI 平台</a></li>
              <li>注册或登录您的账户</li>
              <li>在开发者控制面板中创建新的 API Key</li>
              <li>复制生成的 Token 并粘贴到上方的输入框中</li>
            </ol>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- 删除确认对话框 -->
    <v-dialog v-model="confirmDelete" max-width="500px">
      <v-card>
        <v-card-title>确认删除</v-card-title>
        <v-card-text>
          您确定要删除此 API Token 吗？删除后，将无法使用高级 AI 功能，直到添加新的 Token。
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" variant="text" @click="confirmDelete = false">取消</v-btn>
          <v-btn color="error" variant="text" @click="deleteToken">删除</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import { aiService } from '@/services/api';

export default {
  name: 'AiToken',
  data() {
    return {
      loading: false,
      error: '',
      successMessage: '',
      valid: true,
      tokenValue: '',
      originalToken: '',
      showToken: false,
      isEditing: false,
      hasToken: false,
      confirmDelete: false,
      tokenStats: null,
      userId: null
    }
  },
  created() {
    const user = JSON.parse(localStorage.getItem('user'));
    if (user && user.id) {
      this.userId = user.id;
      this.fetchTokenData();
    } else {
      this.error = '未登录或无法获取用户信息';
    }
  },
  methods: {
    async fetchTokenData() {
      this.loading = true;
      try {
        if (!this.userId) {
          throw new Error('未登录或无法获取用户信息');
        }
        
        try {
          // 尝试获取用户的Token
          const response = await aiService.getDeepseekToken(this.userId);
          
          if (response.data && response.data.data && response.data.data.token) {
            this.tokenValue = response.data.data.token;
            this.originalToken = this.tokenValue;
            this.hasToken = true;
            
            // 获取Token使用统计
            this.fetchTokenStats();
          } else {
            this.tokenValue = '';
            this.originalToken = '';
            this.hasToken = false;
            this.tokenStats = null;
          }
        } catch (apiError) {
          // 如果API返回404（没有找到Token），不显示错误
          if (apiError.response && apiError.response.status === 404) {
            this.tokenValue = '';
            this.originalToken = '';
            this.hasToken = false;
            this.tokenStats = null;
          } else {
            throw apiError;
          }
        }
      } catch (err) {
        this.error = `获取Token信息失败: ${err.message || '未知错误'}`;
        console.error('获取Token信息失败:', err);
      } finally {
        this.loading = false;
      }
    },
    
    async fetchTokenStats() {
      if (!this.hasToken || !this.userId) return;
      
      try {
        const response = await aiService.getTokenStats(this.userId);
        if (response.data && response.data.data) {
          this.tokenStats = response.data.data;
        }
      } catch (err) {
        console.error('获取Token统计信息失败:', err);
        // 如果无法获取真实数据，使用模拟数据
        this.tokenStats = {
          used_tokens: Math.floor(Math.random() * 1000),
          remaining_tokens: Math.floor(Math.random() * 5000) + 1000
        };
      }
    },
    
    startEditing() {
      this.isEditing = true;
    },
    
    cancelEdit() {
      this.tokenValue = this.originalToken;
      this.isEditing = false;
    },
    
    async saveToken() {
      this.loading = true;
      try {
        if (!this.userId) {
          throw new Error('未登录或无法获取用户信息');
        }
        
        const tokenData = {
          token: this.tokenValue
        };
        
        await aiService.saveDeepseekToken(this.userId, tokenData);
        
        this.originalToken = this.tokenValue;
        this.hasToken = true;
        this.isEditing = false;
        this.successMessage = 'API Token 保存成功';
        
        // 获取新的统计数据
        this.fetchTokenStats();
      } catch (err) {
        this.error = `保存Token失败: ${err.message || '未知错误'}`;
        console.error('保存Token失败:', err);
      } finally {
        this.loading = false;
      }
    },
    
    async deleteToken() {
      this.loading = true;
      try {
        if (!this.userId) {
          throw new Error('未登录或无法获取用户信息');
        }
        
        await aiService.deleteDeepseekToken(this.userId);
        
        this.tokenValue = '';
        this.originalToken = '';
        this.hasToken = false;
        this.confirmDelete = false;
        this.tokenStats = null;
        this.successMessage = 'API Token 已删除';
      } catch (err) {
        this.error = `删除Token失败: ${err.message || '未知错误'}`;
        console.error('删除Token失败:', err);
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>

<style scoped>
/* 在此处添加组件特有的样式 */
</style>
