<!-- frontend/src/App.vue -->
<script setup>
import { useAuthStore } from './stores/auth'
const auth = useAuthStore()
</script>

<template>
  <div class="app-layout">
    <!-- 左侧竖向栏 -->
    <aside class="sidebar">
      <h2 class="logo">Mini Blog</h2>
      <template v-if="auth.token">
        <img class="avatar" :src="auth.avatarUrl || '/Users/bruce/vscode/mini_blog/frontend/src/assets/WechatIMG14.jpg'" alt="avatar" />
        <div class="info">
          <p><strong>{{ auth.username }}</strong></p>
          <p>练习项目</p>
        </div>
        <router-link to="/publish" class="publish-btn">发表博客</router-link>
        <router-link to="/me" class="me-btn">我的信息</router-link>
      </template>
      <template v-else>
        <div class="login-hint">
          请先登录以发表文章与发表评论。
          <div class="login-actions">
            <router-link to="/login">登录</router-link>
            <span>或</span>
            <router-link to="/register">注册</router-link>
          </div>
        </div>
      </template>
    </aside>

    <!-- 主体部分 -->
    <div class="main">
      <!-- 顶部横向栏 -->
      <header class="topbar">
        <nav>
          <router-link to="/">首页</router-link>
          <router-link to="/login">登录</router-link>
          <router-link to="/register">注册</router-link>
        </nav>
      </header>

      <!-- 主内容区 -->
      <main class="content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<style>
.app-layout {
  min-height: 100vh;
  font-family: Arial, sans-serif;
}

.sidebar {
  position: fixed;
  left: 0;
  top: 0;
  bottom: 0;
  width: 240px;
  background: linear-gradient(135deg, #e0f7fa 0%, #b4f2b7 100%);
  padding: 24px 20px;
  box-shadow: 2px 0 12px rgba(23, 60, 25, 0.1);
  display: flex;
  flex-direction: column;
  align-items: center;
  transition: box-shadow 0.2s;
  overflow-y: auto;
}
.sidebar:hover {
  box-shadow: 2px 0 24px rgba(29, 74, 31, 0.18);
}

.sidebar .logo {
  margin-bottom: 20px;
}

.sidebar .avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  margin-bottom: 12px;
}

.sidebar .info {
  text-align: center;
  font-size: 14px;
  color: #555;
}

.login-hint {
  margin-top: 8px;
  font-size: 14px;
  color: #355;
  background: rgba(255,255,255,0.6);
  border-radius: 12px;
  padding: 12px;
  text-align: center;
}
.login-actions { display: flex; justify-content: center; align-items: center; gap: 8px; margin-top: 8px; }
.login-actions a { color: #2e7d32; text-decoration: none; padding: 4px 8px; border-radius: 6px; }
.login-actions a:hover { background: rgba(129,199,132,0.25); }

.publish-btn {
  margin-top: 16px;
  width: 100%;
  text-align: center;
  padding: 10px 12px;
  background-color: rgb(244, 251, 243);
  color: #227b3d;
  text-decoration:none;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(56,142,60,0.16);
  transition: transform 0.06s ease, box-shadow 0.2s ease, filter 0.2s ease;
}
.publish-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(56,142,60,0.22);
  filter: brightness(1.02);
}

.me-btn {
  margin-top: 10px;
  width: 100%;
  text-align: center;
  padding: 10px 12px;
  background: rgba(255,255,255,0.85);
  color: #2e7d32;
  text-decoration: none;
  border-radius: 10px;
  box-shadow: inset 0 0 0 1px rgba(129,199,132,0.35);
  transition: transform 0.06s ease, background 0.2s ease;
}
.me-btn:hover {
  transform: translateY(-1px);
  background: rgba(255,255,255,1);
}

.main {
  margin-left: 240px;
  min-height: 100vh;
}

.topbar {
  position: fixed;
  top: 0;
  left: 280px;
  right: 0;
  height: 56px;
  display: flex;
  align-items: center;
  background: rgba(81, 202, 235, 0.72);
  color: #fff;
  padding: 0 20px;
  z-index: 10;
  backdrop-filter: saturate(160%) blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.12);
}

.topbar nav {
  display: flex;
  gap: 10px;
  width: 100%;
  max-width: 1080px;
  margin: 0 auto;
  align-items: center;
}

.topbar a {
  color: #f4f4f4;
  text-decoration: none;
  padding: 8px 12px;
  border-radius: 10px;
  transition: color 0.2s ease, background-color 0.2s ease, transform 0.06s ease;
}

.topbar a:hover {
  background: rgba(255, 255, 255, 0.10);
  color: #ffffff;
  transform: translateY(-1px);
}

.topbar a.router-link-active {
  background: linear-gradient(135deg, rgba(129, 199, 132, 0.35), rgba(76, 175, 80, 0.28));
  color: #ffffff;
  box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.12);
}

.content {
  padding: 20px;
  padding-top: 76px; /* 56px 顶部栏高度 + 间距 */
}

/* 移动端响应式 */
@media (max-width: 768px) {
  .sidebar {
    position: static;
    width: auto;
    padding: 12px;
    margin: 0;
    border-radius: 0;
    box-shadow: none;
    background: linear-gradient(135deg, #e0f7fa 0%, #c8e6c9 100%);
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
  }
  .sidebar .avatar { width: 40px; height: 40px; }
  .sidebar .info { font-size: 12px; }
  .publish-btn, .me-btn { width: auto; padding: 8px 10px; margin-top: 0; }

  .main { margin-left: 0; }
  .topbar { left: 0; }
  .content { padding: 16px; padding-top: 72px; }
}
</style>