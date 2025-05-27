<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="10" md="8">
        <v-card class="elevation-12">
          <v-toolbar color="primary" dark flat>
            <v-toolbar-title>注册</v-toolbar-title>
            <v-spacer></v-spacer>
          </v-toolbar>
          <v-card-text>
            <v-form ref="form" v-model="valid" @submit.prevent="register">
              <v-row>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="username"
                    :rules="usernameRules"
                    label="用户名"
                    prepend-icon="mdi-account"
                    required
                  ></v-text-field>
                </v-col>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="email"
                    :rules="emailRules"
                    label="邮箱"
                    prepend-icon="mdi-email"
                    type="email"
                    required
                  ></v-text-field>
                </v-col>
              </v-row>
              
              <v-row>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="password"
                    :rules="passwordRules"
                    :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                    :type="showPassword ? 'text' : 'password'"
                    label="密码"
                    prepend-icon="mdi-lock"
                    @click:append="showPassword = !showPassword"
                    required
                  ></v-text-field>
                </v-col>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="confirmPassword"
                    :rules="confirmPasswordRules"
                    :append-icon="showConfirmPassword ? 'mdi-eye' : 'mdi-eye-off'"
                    :type="showConfirmPassword ? 'text' : 'password'"
                    label="确认密码"
                    prepend-icon="mdi-lock-check"
                    @click:append="showConfirmPassword = !showConfirmPassword"
                    required
                  ></v-text-field>
                </v-col>
              </v-row>
              
              <v-row>
                <v-col cols="12" md="4">
                  <v-select
                    v-model="gender"
                    :items="genderOptions"
                    label="性别"
                    prepend-icon="mdi-gender-male-female"
                  ></v-select>
                </v-col>
                <v-col cols="12" md="4">
                  <v-text-field
                    v-model="age"
                    :rules="ageRules"
                    label="年龄"
                    prepend-icon="mdi-calendar"
                    type="number"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" md="4">
                  <v-text-field
                    v-model="height"
                    :rules="heightRules"
                    label="身高(cm)"
                    prepend-icon="mdi-human-male-height"
                    type="number"
                    step="0.1"
                  ></v-text-field>
                </v-col>
              </v-row>
              
              <v-row>
                <v-col cols="12" md="4">
                  <v-text-field
                    v-model="weight"
                    :rules="weightRules"
                    label="体重(kg)"
                    prepend-icon="mdi-scale-bathroom"
                    type="number"
                    step="0.1"
                  ></v-text-field>
                </v-col>
              </v-row>
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
            <v-btn color="secondary" variant="text" @click="goToLogin">返回登录</v-btn>
            <v-btn color="primary" :loading="loading" :disabled="!valid || loading" @click="register">注册</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { userService } from '@/services/api';

export default {
  name: 'Register',
  data() {
    return {
      valid: false,
      loading: false,
      error: '',
      username: '',
      email: '',
      password: '',
      confirmPassword: '',
      showPassword: false,
      showConfirmPassword: false,
      gender: 1,
      age: '',
      height: '',
      weight: '',
      genderOptions: [
        { title: '男', value: 1 },
        { title: '女', value: 2 },
        { title: '未指定', value: 0 }
      ],
      usernameRules: [
        v => !!v || '用户名不能为空',
        v => (v && v.length >= 4 && v.length <= 20) || '用户名长度需要在4-20个字符之间'
      ],
      emailRules: [
        v => !!v || '邮箱不能为空',
        v => /.+@.+\..+/.test(v) || '请输入有效的邮箱地址'
      ],
      passwordRules: [
        v => !!v || '密码不能为空',
        v => (v && v.length >= 6) || '密码至少需要6个字符'
      ],
      confirmPasswordRules: [
        v => !!v || '确认密码不能为空',
        v => v === this.password || '两次输入的密码不一致'
      ],
      ageRules: [
        v => !v || (v >= 1 && v <= 120) || '请输入有效的年龄(1-120)'
      ],
      heightRules: [
        v => !v || (v >= 50 && v <= 250) || '请输入有效的身高(50-250cm)'
      ],
      weightRules: [
        v => !v || (v >= 20 && v <= 300) || '请输入有效的体重(20-300kg)'
      ]
    };
  },
  methods: {
    async register() {
      if (!this.$refs.form.validate()) return;
      
      this.loading = true;
      this.error = '';
      
      try {
        const userData = {
          username: this.username,
          password: this.password,
          email: this.email,
          gender: this.gender,
          age: this.age ? parseInt(this.age) : null,
          height: this.height ? parseFloat(this.height) : null,
          weight: this.weight ? parseFloat(this.weight) : null
        };
        
        const response = await userService.register(userData);
        
        if (response.data.code === 201 || response.status === 201) {
          // 注册成功，跳转到登录页
          this.$router.push({ 
            name: 'Login', 
            query: { registered: 'true' }, 
            params: { username: this.username } 
          });
        } else {
          this.error = response.data.message || '注册失败';
        }
      } catch (error) {
        this.error = error.response?.data?.error || '注册失败，请稍后再试';
        console.error('注册错误:', error);
      } finally {
        this.loading = false;
      }
    },
    goToLogin() {
      this.$router.push({ name: 'Login' });
    }
  }
};
</script>
