<!-- frontend/src/pages/Login.vue -->
<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'
import { useAuthStore } from '../stores/auth'

const username = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)
const router = useRouter()
const auth = useAuthStore()

async function login() {
  error.value = ''
  loading.value = true
  try {
    const { data } = await api.post('/login', { username: username.value, password: password.value })
    // 登录后拉取头像
    let avatarUrl = ''
    try {
      const me = await api.get('/me')
      avatarUrl = me.data?.avatar_url || ''
    } catch (e) {}
    auth.setAuth(data.access_token, data.username, avatarUrl)
    router.push('/')
  } catch (err) {
    error.value = err.response?.data?.message || '登录失败'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="login-bg">
    <div class="login-container">
      <h2 class="login-title">登录</h2>
      <div v-if="error" class="login-error">{{ error }}</div>
      <div class="login-field">
        <input v-model="username" placeholder="用户名" class="login-input" />
      </div>
      <div class="login-field">
        <input v-model="password" type="password" placeholder="密码" class="login-input" />
      </div>
      <button @click="login" :disabled="loading" class="login-btn">
        {{ loading ? '登录中...' : '登录' }}
      </button>
    </div>
  </div>
</template>

<style scoped>
.login-bg {
  min-height: calc(100vh - 76px);
  background: linear-gradient(135deg, #e0f7fa 0%, #c8e6c9 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}
.login-container {
  background: linear-gradient(135deg, #f1f8e9 0%, #e0f2f1 100%);
  border-radius: 16px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.10);
  padding: 50px 36px 32px 36px;
  min-width: 340px;
  max-width: 380px;
  width: 100%;
  /* margin-top: -250px; */
}
.login-title {
  font-size: 1.7rem;
  font-weight: 700;
  color: #388e3c;
  text-align: center;
  margin-bottom: 28px;
}
.login-error {
  color: #d32f2f;
  background: #fff3f3;
  border-radius: 6px;
  padding: 8px 12px;
  margin-bottom: 18px;
  text-align: center;
  font-size: 1rem;
}
.login-field {
  margin-bottom: 18px;
}
.login-input {
  width: 100%;
  padding: 12px 14px;
  border: 1px solid #c8e6c9;
  border-radius: 8px;
  font-size: 1.05rem;
  background: #f8f9fa;
  transition: border-color 0.2s;
}
.login-input:focus {
  outline: none;
  border-color: #388e3c;
  background: #e0f2f1;
}
.login-btn {
  width: 100%;
  padding: 12px 0;
  background: linear-gradient(90deg, #81c784 0%, #4caf50 100%);
  color: #fff;
  font-size: 1.15rem;
  font-weight: 600;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(56,142,60,0.08);
  transition: background 0.2s, box-shadow 0.2s;
}
.login-btn:disabled {
  background: #bdbdbd;
  cursor: not-allowed;
}
.login-btn:hover:not(:disabled) {
  background: linear-gradient(90deg, #66bb6a 0%, #388e3c 100%);
  box-shadow: 0 4px 16px rgba(56,142,60,0.12);
}

@media (max-width: 768px) {
  .login-container { min-width: auto; width: calc(100% - 20px); margin: 0 10px; padding: 32px 18px; }
}
</style>