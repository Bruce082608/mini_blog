<!-- frontend/src/pages/Me.vue -->
<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const auth = useAuthStore()

const profile = ref({ username: '', avatar_url: '' })
const myArticles = ref([])
const loading = ref(true)
const saving = ref(false)
const msg = ref('')
const err = ref('')

async function load() {
  if (!auth.token) { router.push('/login'); return }
  loading.value = true
  try {
    const [meRes, artsRes] = await Promise.all([
      api.get('/me'),
      api.get('/me/articles'),
    ])
    profile.value = meRes.data
    myArticles.value = artsRes.data
  } finally {
    loading.value = false
  }
}

async function save() {
  err.value = ''
  msg.value = ''
  saving.value = true
  try {
    await api.patch('/me', { username: profile.value.username, avatar_url: profile.value.avatar_url })
    msg.value = '保存成功'
    // 同步全局用户名
    if (auth.username !== profile.value.username) {
      auth.setAuth(auth.token, profile.value.username, profile.value.avatar_url)
    }
  } catch (e) {
    err.value = e.response?.data?.message || '保存失败'
  } finally {
    saving.value = false
  }
}

async function onFileChange(e) {
  const file = e.target.files && e.target.files[0]
  if (!file) return
  const fd = new FormData()
  fd.append('file', file)
  try {
    const { data } = await api.post('/me/avatar', fd, { headers: { 'Content-Type': 'multipart/form-data' } })
    profile.value.avatar_url = data.url
    // 同步全局用户名不变，仅头像变更
    auth.setAvatar(data.url)
  } catch (e2) {
    err.value = e2.response?.data?.message || '上传失败'
  }
}

onMounted(load)
</script>

<template>
  <div class="me">
    <div v-if="loading">加载中...</div>
    <div v-else>
      <h2>我的信息</h2>
      <div class="card">
        <div class="row">
          <div class="col avatar-col">
            <img v-if="profile.avatar_url" :src="profile.avatar_url" class="avatar" alt="avatar" />
            <div v-else class="avatar placeholder">无头像</div>
            <label class="upload-btn">
              更换头像
              <input type="file" accept="image/*" @change="onFileChange" />
            </label>
          </div>
          <div class="col form-col">
            <div class="field">
              <label>头像 URL</label>
              <input v-model="profile.avatar_url" placeholder="请输入头像图片地址(支持 http/https)" />
            </div>
            <div class="field">
              <label>用户名</label>
              <input v-model="profile.username" placeholder="请输入用户名" />
            </div>
            <div class="actions">
              <button @click="save" :disabled="saving">{{ saving ? '保存中...' : '保存' }}</button>
            </div>
            <div v-if="msg" class="msg success">{{ msg }}</div>
            <div v-if="err" class="msg error">{{ err }}</div>
          </div>
        </div>
      </div>

      <section class="list">
        <h3>我发表的文章</h3>
        <ul v-if="myArticles.length" class="article-list">
          <li v-for="a in myArticles" :key="a.id">
            <router-link :to="`/article/${a.id}`">{{ a.title }}</router-link>
            <span class="time">{{ new Date(a.created_at).toLocaleString() }}</span>
          </li>
        </ul>
        <div v-else class="empty">还没有发表过文章</div>
      </section>
    </div>
  </div>
</template>

<style scoped>
.me { max-width: 960px; margin: 0 auto; }

.card { background: #fff; border: 1px solid #e6e6e6; border-radius: 12px; padding: 16px; }

.row { display: grid; grid-template-columns: 180px 1fr; gap: 16px; }

.avatar { width: 160px; height: 160px; border-radius: 12px; object-fit: cover; }

.avatar.placeholder { display:flex; align-items:center; justify-content:center; background:#f1f1f1; color:#888; }

.upload-btn { margin-top: 8px; display:inline-block; padding:6px 10px; background:#fff; border:1px solid #c8e6c9; border-radius:8px; color:#2e7d32; cursor:pointer; font-size: 14px; }
.upload-btn input { display:none; }

.field { margin-bottom: 12px; display:flex; flex-direction:column; gap:6px; }

label { font-weight: 600; color: #444; }
input { padding: 10px 12px; border: 1px solid #c8e6c9; border-radius: 8px; background: #f8f9fa; }

.actions { margin-top: 8px; }

button { padding: 8px 14px; border:none; border-radius:8px; background: linear-gradient(90deg,#81c784,#4caf50); color:#fff; cursor:pointer; }

.msg { padding: 8px 12px; border-radius: 6px; margin-top: 8px; }

.msg.success { color:#2e7d32; background:#e8f5e9; }

.msg.error { color:#d32f2f; background:#fff3f3; }

.list { margin-top: 18px; }

.article-list { list-style: none; padding: 0; }

.article-list li { padding: 10px 0; border-bottom: 1px solid #eee; display:flex; justify-content:space-between; align-items:center; }

.time { color:#999; font-size:12px; }

@media (max-width: 768px) {
  .card { border-radius: 10px; padding: 14px; }
  .row { grid-template-columns: 1fr; }
  .avatar { width: 120px; height: 120px; }
}
</style>


