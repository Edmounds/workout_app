<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="6">
        <v-card class="text-center pa-6">
          <v-card-title class="text-h4 font-weight-bold">404</v-card-title>
          <v-card-subtitle class="text-h6 mt-2">页面未找到</v-card-subtitle>
          <v-card-text>
            <p class="mb-4">您请求的页面不存在或已被移除。</p>
            <v-img
              src="https://cdn.vuetifyjs.com/images/pages/404.svg"
              alt="404 Not Found"
              height="200"
              contain
              class="my-4"
            ></v-img>
          </v-card-text>
          <v-card-actions class="justify-center">
            <v-btn color="primary" variant="flat" @click="goHome">返回首页</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'NotFound',
  methods: {
    goHome() {
      this.$router.push({ name: 'Dashboard' });
    }
  }
}
</script>
