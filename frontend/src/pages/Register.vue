<!-- frontend/src/pages/Register.vue -->
<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'

const username = ref('')
const password = ref('')
const error = ref('')
const success = ref('')
const loading = ref(false)
const router = useRouter()

async function register() {
  error.value = ''
  success.value = ''
  loading.value = true
  try {
    await api.post('/register', { username: username.value, password: password.value })
    success.value = '注册成功，请登录'
    setTimeout(() => router.push('/login'), 1000)
  } catch (err) {
    error.value = err.response?.data?.message || '注册失败'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="register-bg">
    <div class="register-container">
      <h2 class="register-title">注册</h2>
      <div v-if="error" class="register-error">{{ error }}</div>
      <div v-if="success" class="register-success">{{ success }}</div>
      <div class="register-field">
        <input v-model="username" placeholder="用户名" class="register-input" />
      </div>
      <div class="register-field">
        <input v-model="password" type="password" placeholder="密码" class="register-input" />
      </div>
      <button @click="register" :disabled="loading" class="register-btn">
        {{ loading ? '注册中...' : '注册' }}
      </button>
    </div>
  </div>
</template>

<style scoped>
.register-bg {
  min-height: calc(100vh - 76px);
  background: linear-gradient(135deg, #e0f7fa 0%, #c8e6c9 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}
.register-container {
  background: linear-gradient(135deg, #f1f8e9 0%, #e0f2f1 100%);
  border-radius: 16px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.10);
  padding: 40px 36px 32px 36px;
  min-width: 340px;
  max-width: 380px;
  width: 100%;
}
.register-title {
  font-size: 1.7rem;
  font-weight: 700;
  color: #388e3c;
  text-align: center;
  margin-bottom: 28px;
}
.register-error {
  color: #d32f2f;
  background: #fff3f3;
  border-radius: 6px;
  padding: 8px 12px;
  margin-bottom: 18px;
  margin-left: 15px;
  text-align: center;
  font-size: 1rem;
}
.register-success {
  color: #388e3c;
  background: #e8f5e9;
  border-radius: 6px;
  padding: 8px 12px;
  margin-bottom: 18px;
  text-align: center;
  font-size: 1rem;
}
.register-field {
  margin-bottom: 18px;
}
.register-input {
  width: 100%;
  padding: 12px 14px;
  border: 1px solid #c8e6c9;
  border-radius: 8px;
  font-size: 1.05rem;
  background: #f8f9fa;
  transition: border-color 0.2s;
}
.register-input:focus {
  outline: none;
  border-color: #388e3c;
  background: #e0f2f1;
}
.register-btn {
  width: 100%;
  margin-left: 2px;
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
.register-btn:disabled {
  background: #bdbdbd;
  cursor: not-allowed;
}
.register-btn:hover:not(:disabled) {
  background: linear-gradient(90deg, #66bb6a 0%, #388e3c 100%);
  box-shadow: 0 4px 16px rgba(56,142,60,0.12);
}

@media (max-width: 768px) {
  .register-container { min-width: auto; width: calc(100% - 20px); margin: 0 10px; padding: 32px 18px; }
}
</style>