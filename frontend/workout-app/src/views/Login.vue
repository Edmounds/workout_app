<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="4">
        <v-card class="elevation-12">
          <v-toolbar color="primary" dark flat>
            <v-toolbar-title>登录</v-toolbar-title>
            <v-spacer></v-spacer>
          </v-toolbar>
          <v-card-text>
            <v-form ref="form" v-model="valid" @submit.prevent="login">
              <v-text-field
                v-model="username"
                :rules="usernameRules"
                label="用户名"
                name="username"
                prepend-icon="mdi-account"
                type="text"
                required
              ></v-text-field>

              <v-text-field
                v-model="password"
                :rules="passwordRules"
                :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                :type="showPassword ? 'text' : 'password'"
                label="密码"
                name="password"
                prepend-icon="mdi-lock"
                @click:append="showPassword = !showPassword"
                required
              ></v-text-field>
            </v-form>
            <v-alert
              v-if="error"
              type="error"
              class="mt-3"
              closable
              @click:close="error = ''"
            >
              {{ error }}
            </v-alert>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="secondary" variant="text" @click="goToRegister">注册</v-btn>
            <v-btn color="primary" :loading="loading" :disabled="!valid || loading" @click="login">登录</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { userService } from '@/services/api';

export default {
  name: 'Login',
  data() {
    return {
      valid: false,
      loading: false,
      error: '',
      username: '',
      password: '',
      showPassword: false,
      usernameRules: [
        v => !!v || '用户名不能为空',
        v => (v && v.length >= 4) || '用户名至少需要4个字符',
      ],
      passwordRules: [
        v => !!v || '密码不能为空',
        v => (v && v.length >= 6) || '密码至少需要6个字符',
      ],
    };
  },
  methods: {
    async login() {
      if (!this.$refs.form.validate()) return;
      
      this.loading = true;
      this.error = '';
      
      try {
        const credentials = {
          username: this.username,
          password: this.password
        };
        
        const response = await userService.login(credentials);
        
        if (response.data.code === 200) {
          // 登录成功，存储用户信息
          const userData = response.data.data;
          localStorage.setItem('user', JSON.stringify(userData));
          
          // 跳转到首页或重定向页面
          const redirectPath = this.$route.query.redirect || '/';
          this.$router.push(redirectPath);
        } else {
          this.error = response.data.message || '登录失败';
        }
      } catch (error) {
        this.error = error.response?.data?.error || '登录失败，请检查您的用户名和密码';
        console.error('登录错误:', error);
      } finally {
        this.loading = false;
      }
    },
    goToRegister() {
      this.$router.push({ name: 'Register' });
    }
  }
};
</script>
