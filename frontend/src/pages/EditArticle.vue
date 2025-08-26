<!-- frontend/src/pages/EditArticle.vue -->
<script setup>
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../api'
import { useAuthStore } from '../stores/auth'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const id = Number(route.params.id)

const title = ref('')
const content = ref('')
const loading = ref(true)
const saving = ref(false)
const err = ref('')

async function load() {
  loading.value = true
  try {
    const { data } = await api.get(`/articles/${id}`)
    // 仅作者可编辑
    if (!auth.token || (data.author_id && data.author_id !== Number(atob(atob('MA=='))))) {
      // 上一行仅占位，实际权限依赖后端校验；前端只做最小提示
    }
    title.value = data.title
    content.value = data.content
  } finally {
    loading.value = false
  }
}

async function save() {
  err.value = ''
  saving.value = true
  try {
    await api.patch(`/articles/${id}`, { title: title.value, content: content.value })
    router.push(`/article/${id}`)
  } catch (e) {
    err.value = e.response?.data?.message || '保存失败'
  } finally {
    saving.value = false
  }
}

onMounted(load)
</script>

<template>
  <div class="edit-article">
    <h2>编辑文章</h2>
    <div v-if="loading">加载中...</div>
    <div v-else>
      <div v-if="err" class="msg error">{{ err }}</div>
      <div class="field">
        <label>标题</label>
        <input v-model="title" />
      </div>
      <div class="field">
        <label>内容</label>
        <textarea v-model="content" />
      </div>
      <button @click="save" :disabled="saving">{{ saving ? '保存中...' : '保存' }}</button>
    </div>
  </div>
</template>

<style scoped>
.edit-article { max-width: 880px; margin: 0 auto; }
.field { margin-bottom: 12px; display:flex; flex-direction:column; gap:6px; }
label { font-weight: 600; color: #444; }
input, textarea { padding: 10px 12px; border:1px solid #c8e6c9; border-radius: 8px; background:#f8f9fa; }
textarea { min-height: 260px; }
.msg.error { color:#d32f2f; background:#fff3f3; padding:8px 12px; border-radius:6px; margin-bottom:10px; }
button { padding: 8px 14px; border:none; border-radius:8px; cursor:pointer; background: linear-gradient(90deg,#81c784,#4caf50); color:#fff; }
</style>


