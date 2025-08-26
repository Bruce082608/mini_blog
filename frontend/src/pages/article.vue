<!-- frontend/src/pages/Article.vue -->
<script setup>
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import api from '../api'
import { useAuthStore } from '../stores/auth'

const route = useRoute()
const id = Number(route.params.id)
const article = ref(null)
const comments = ref([])
const content = ref('')
const loading = ref(true)
const posting = ref(false)
const auth = useAuthStore()

async function removeArticle() {
  if (!confirm('确定要删除这篇文章吗？此操作不可恢复。')) return
  await api.delete(`/articles/${id}`)
  window.location.href = '/'
}

async function load() {
  loading.value = true
  const [a, c] = await Promise.all([
    api.get(`/articles/${id}`),
    api.get(`/articles/${id}/comments`),
  ])
  article.value = a.data
  comments.value = c.data
  loading.value = false
}

async function submitComment() {
  if (!content.value.trim()) return
  posting.value = true
  try {
    await api.post(`/articles/${id}/comments`, { content: content.value })
    content.value = ''
    await load()
  } finally {
    posting.value = false
  }
}

onMounted(load)
</script>

<template>
  <div class="article">
    <div v-if="loading">加载中...</div>
    <div v-else>
      <div class="header">
        <h1 class="title">{{ article.title }}</h1>
        <div class="meta">
          作者：{{ article.author || '匿名作者' }} · {{ new Date(article.created_at).toLocaleString() }}
        </div>
        <div v-if="auth.username && article.author && auth.username === article.author" class="owner-actions">
          <router-link :to="`/article/${id}/edit`" class="edit-btn">编辑</router-link>
          <button class="delete-btn" @click="removeArticle">删除</button>
        </div>
      </div>
      <div class="content-card">
        <div class="content">{{ article.content }}</div>
      </div>

      <section class="comments">
        <h3>评论</h3>
        <ul v-if="comments.length" class="comment-list">
          <li v-for="c in comments" :key="c.id" class="comment-item">
            <div class="comment-card">
              <div class="comment-head">
                <strong class="user">{{ c.user }}</strong>
                <span class="time">{{ new Date(c.created_at).toLocaleString() }}</span>
              </div>
              <p class="comment-body">{{ c.content }}</p>
            </div>
          </li>
        </ul>
        <div v-else class="empty">还没有评论，快来抢沙发吧！</div>

        <div v-if="auth.token" class="comment-form">
          <textarea v-model="content" placeholder="写下你的评论..." />
          <div class="form-actions">
            <button @click="submitComment" :disabled="posting">
              {{ posting ? '提交中...' : '发表评论' }}
            </button>
          </div>
        </div>
        <div v-else class="login-tip">
          请先 <router-link to="/login">登录</router-link> 后发表评论。
        </div>
      </section>
    </div>
  </div>
</template>

<style scoped>
.article {
  max-width: 800px;
  margin: 0 auto;
}

.title {
  font-size: 32px;
  font-weight: bold;
  margin-bottom: 8px;
}

.meta {
  font-size: 13px;
  color: #888;
  margin-bottom: 16px;
}

.content {
  font-size: 18px;
  line-height: 1.6;
  margin-bottom: 24px;
}

.comments h3 {
  margin-bottom: 12px;
}

.comment-list {
  list-style: none;
  padding: 0;
}

.comment-item {
  padding: 12px 0;
  border-bottom: 1px solid #eee;
}

.comment-item .time {
  font-size: 12px;
  color: #999;
  margin-left: 6px;
}

.comment-form {
  margin-top: 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.comment-form textarea {
  width: 100%;
  min-height: 80px;
  padding: 8px;
}

.comment-form button {
  align-self: flex-end;
  padding: 6px 12px;
  cursor: pointer;
}

.login-tip {
  margin-top: 16px;
  color: #666;
}

/* ---- Enhanced layout overrides ---- */
.article { max-width: 880px; }
.header { margin-bottom: 10px; }
.title { font-size: 30px; font-weight: 800; margin: 0; letter-spacing: 0.2px; }
.meta { margin-top: 6px; }
.owner-actions { margin-top: 10px; display:flex; gap: 10px; }
.edit-btn { padding: 6px 10px; border-radius:8px; text-decoration:none; color:#1b5e20; background:rgba(129,199,132,0.25); }
.edit-btn:hover { background:rgba(129,199,132,0.35); }
.delete-btn { padding: 6px 10px; border:none; border-radius:8px; color:#fff; background:#e53935; cursor:pointer; }
.delete-btn:hover { filter: brightness(0.95); }

.content-card {
  background: #fff;
  border: 1px solid #eaeaea;
  border-radius: 14px;
  padding: 22px 22px;
  box-shadow: 0 6px 22px rgba(0,0,0,0.06);
  margin: 14px 0 26px;
}
.content { font-size: 17px; line-height: 1.9; color: #2b2b2b; white-space: pre-wrap; }

.comment-list { list-style: none; padding: 0; display: flex; flex-direction: column; gap: 12px; }
.comment-item { padding: 0; border: none; }
.comment-card {
  background: linear-gradient(180deg, #f7fdf8, #ffffff);
  border: 1px solid #e3f1e5;
  border-radius: 12px;
  padding: 12px 14px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.04);
}
.comment-head { display: flex; align-items: center; gap: 8px; margin-bottom: 6px; }
.comment-head .user { color: #2e7d32; }
.comment-head .time { font-size: 12px; color: #9aa0a6; }
.comment-body { margin: 6px 0 2px; color: #333; line-height: 1.7; }

.comment-form textarea { width: 100%; min-height: 96px; padding: 10px 12px; border: 1px solid #c8e6c9; border-radius: 10px; background: #f8f9fa; }
.form-actions { display: flex; justify-content: flex-end; }
.comment-form button { padding: 8px 14px; cursor: pointer; border: none; border-radius: 8px; background: linear-gradient(90deg, #81c784, #4caf50); color: #fff; }
@media (max-width: 768px) {
  .article { padding: 0 6px; }
  .title { font-size: 22px; }
  .content-card { padding: 16px; }
  .comment-card { padding: 10px 12px; }
  .comment-form textarea { min-height: 80px; }
}
</style>