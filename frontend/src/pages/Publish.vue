<!-- frontend/src/pages/Publish.vue -->
<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const auth = useAuthStore()
const title = ref('')
const content = ref('')
const error = ref('')
const success = ref('')
const submitting = ref(false)

async function submit() {
  error.value = ''
  success.value = ''
  if (!title.value.trim() || !content.value.trim()) {
    error.value = '标题和内容不能为空'
    return
  }
  if (!auth.token) {
    router.push('/login')
    return
  }
  submitting.value = true
  try {
    const { data } = await api.post('/articles', { title: title.value, content: content.value })
    success.value = '发表成功'
    setTimeout(() => router.push(`/article/${data.id}`), 600)
  } catch (e) {
    error.value = e.response?.data?.message || '发表失败'
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <div class="publish">
    <h2>发表博客</h2>
    <div v-if="error" class="msg error">{{ error }}</div>
    <div v-if="success" class="msg success">{{ success }}</div>

    <div class="field">
      <label>标题</label>
      <input v-model="title" placeholder="请输入文章标题" />
    </div>

    <div class="field">
      <label>内容</label>
      <textarea v-model="content" placeholder="写点什么..." />
    </div>

    <button @click="submit" :disabled="submitting">
      {{ submitting ? '提交中...' : '发表' }}
    </button>
  </div>
  
</template>

<style scoped>
.publish {
  max-width: 860px;
  margin: 0 auto;
}
.field { margin-bottom: 16px; display: flex; flex-direction: column; gap: 8px; }
label { font-weight: 600; color: #444; }
input, textarea {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #c8e6c9;
  border-radius: 8px;
  background: #f8f9fa;
}
textarea { min-height: 220px; }
.msg { padding: 8px 12px; border-radius: 6px; margin-bottom: 12px; }
.msg.error { color: #d32f2f; background: #fff3f3; }
.msg.success { color: #2e7d32; background: #e8f5e9; }
button {
  padding: 10px 16px; cursor: pointer; border: none; border-radius: 8px;
  color: #fff; background: linear-gradient(90deg, #81c784, #4caf50);
}
button:disabled { background: #bdbdbd; cursor: not-allowed; }

@media (max-width: 768px) {
  .publish { padding: 0 6px; }
  textarea { min-height: 180px; }
}
</style>


