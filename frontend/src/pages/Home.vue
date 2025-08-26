<!-- frontend/src/pages/Home.vue -->
<script setup>
import { onMounted, ref } from 'vue'
import api from '../api'

const articles = ref([])
const loading = ref(true)

onMounted(async () => {
  const { data } = await api.get('/articles')
  articles.value = data
  loading.value = false
})
</script>

<template>
  <div class="home">
    <h2>文章列表</h2>
    <div v-if="loading">加载中...</div>
    <ul v-else class="article-list grid">
      <li v-for="a in articles" :key="a.id" class="article-card">
        <router-link :to="`/article/${a.id}`" class="title">{{ a.title }}</router-link>
        <div class="meta">作者：{{ a.author || '匿名作者' }} · {{ new Date(a.created_at).toLocaleString() }}</div>
        <p class="excerpt">{{ a.excerpt }}</p>
        <div class="actions">
          <router-link :to="`/article/${a.id}`" class="readmore">阅读全文</router-link>
        </div>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.home {
  max-width: 800px;
  margin: 0 auto;
}

.article-list { list-style: none; padding: 0; }
.article-list.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 16px;
}

.article-card {
  background: #fff;
  border: 1px solid #eaeaea;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.04);
  transition: transform 0.08s ease, box-shadow 0.2s ease;
  display: flex;
  flex-direction: column;
  min-height: 160px;
}
.article-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 22px rgba(0,0,0,0.08);
}

.article-card .title {
  font-size: 18px;
  font-weight: 700;
  color: #2b2b2b;
  text-decoration: none;
}
.article-card .title:hover { text-decoration: underline; }
.article-card .meta { font-size: 12px; color: #888; margin: 6px 0 8px; }
.article-card .excerpt { color: #555; flex: 1; }
.actions { margin-top: 12px; }
.readmore { font-size: 14px; color: #2e7d32; text-decoration: none; }
.readmore:hover { text-decoration: underline; }

@media (max-width: 768px) {
  .home { padding: 0 6px; }
  .article-list.grid { grid-template-columns: 1fr; gap: 12px; }
  .article-card { padding: 14px; }
  .article-card .title { font-size: 17px; }
}
</style>