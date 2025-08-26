# Mini Blog 全栈项目

一个基于 Flask（后端）与 Vue 3（前端）的极简个人博客示例，支持注册/登录（JWT）、文章列表与详情、评论、发表文章、作者专属的编辑/删除、个人资料与头像上传；已配置 CORS 与 Vite allowedHosts 支持本地与 ngrok 联调。

## 目录结构

```
mini_blog/
  backend/
    app.py                # Flask 应用入口与路由
    models.py             # SQLAlchemy 模型（User/Article/Comment）
    instance/
      blog.db             # SQLite 数据库（运行后生成/更新）
    requirements.txt      # Python 依赖
  frontend/
    index.html            # 前端入口 HTML
    src/
      main.js             # 前端入口文件
      App.vue             # 全局布局（左侧固定侧栏 + 顶部固定导航）
      router/index.js     # 路由定义：Home / Article / Login / Register / Publish / Me / ArticleEdit
      api/index.js        # Axios 实例与请求拦截器（自动带上 Bearer Token）
      stores/auth.js      # Pinia 鉴权状态（token/username/avatarUrl 持久化到 localStorage）
      pages/
        Home.vue          # 文章列表页
        Article.vue       # 文章详情与评论区
        Login.vue         # 登录页
        Register.vue      # 注册页
        Publish.vue       # 发表文章页（登录后可用）
        Me.vue            # 我的信息（用户名、头像上传、我的文章）
        EditArticle.vue   # 编辑文章页（仅作者可用）
    package.json          # 前端脚本与依赖
    vite.config.js        # Vite 配置
  （运行时）backend/uploads/     # 头像上传目录，经由 /uploads/* 提供静态访问
```

## 技术栈

- 后端：Flask、Flask-SQLAlchemy、Flask-JWT-Extended、Flask-CORS、SQLite
- 前端：Vue 3、Vite、Pinia、Vue Router、Axios

## 环境要求

- Node.js ≥ 18（建议）
- Python ≥ 3.10（建议）

## 启动步骤

### 1) 后端（Flask）

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 可选：设置 JWT 密钥（生产环境务必更改）
export JWT_SECRET_KEY="your-strong-secret"  # Windows PowerShell: $env:JWT_SECRET_KEY="..."

python app.py  # 启动 http://localhost:5000
```

- 健康检查：`http://localhost:5000/api/health`
- 首次启动会自动创建 SQLite 数据库并插入两篇示例文章。

### 2) 前端（Vite + Vue 3）

```bash
cd frontend
npm install
npm run dev  # 启动 http://localhost:5173
```

- Axios 基础地址：`http://localhost:5000/api`
- 请求拦截器自动为已登录用户附带 `Authorization: Bearer <token>`

## 使用说明

1. 访问 `http://localhost:5173` 查看文章列表。
2. 点击文章进入详情页浏览内容与评论。
3. 注册并登录后：
   - 可在文章详情页发表评论；
   - 可通过左侧“发表博客”创建新文章；
   - 在“我的信息”中编辑用户名、上传头像，并查看/管理自己发表的文章；
   - 自己的文章在详情页可“编辑/删除”。

> CORS 允许来源在 `backend/app.py` 的 `CORS(app, resources=..., origins=[...])` 中配置，默认包含 `http://localhost:5173` 与 `http://127.0.0.1:5173`。

## 后端 API 概览

- POST `/api/register`：注册
  - Body: `{ "username": string, "password": string }`
- POST `/api/login`：登录
  - Response: `{ "access_token": string, "username": string }`
- GET `/api/articles`：文章列表（含 `excerpt`）
- GET `/api/articles/:id`：文章详情（含 `author`, `author_id`）
- GET `/api/articles/:id/comments`：评论列表
- POST `/api/articles/:id/comments`：发表评论（需携带 JWT）
  - Header: `Authorization: Bearer <token>`
  - Body: `{ "content": string }`
  
- POST `/api/articles`：发表文章（需携带 JWT）
- PATCH `/api/articles/:id`：更新文章（仅作者可操作）
- DELETE `/api/articles/:id`：删除文章（仅作者可操作）

- GET `/api/me`：获取我的资料
- PATCH `/api/me`：更新我的资料（用户名、头像 URL）
- POST `/api/me/avatar`：上传头像文件（返回头像 URL）
- GET `/api/me/articles`：获取我发表的文章

## 关键实现与约定

- 布局：`App.vue` 实现左侧固定侧栏与顶部固定导航，内容区自适应剩余空间。
- 鉴权：`stores/auth.js` 持久化 `token` 与 `username` 到 `localStorage`；`api/index.js` 在请求阶段自动读取并注入到请求头。
- 数据库：使用 SQLite（`backend/instance/blog.db`）；可直接删除该文件完成“重置”。

## 常见问题（FAQ）

- 跨域错误（CORS）：
  - 确认后端已运行在 `:5000`，前端在 `:5173`。
  - 检查 `backend/app.py` 中 `CORS` 的 `origins` 是否包含你的前端地址。
- 登录后仍返回 401：
  - 打开浏览器 Network 面板，确认请求头包含 `Authorization: Bearer <token>`。
  - 确认登录成功后 Pinia 已存储 `token`（`localStorage`）。
- 数据库为空/想要重置数据：
  - 删除 `backend/instance/blog.db` 后重启后端，系统会重新创建并注入示例数据。

## 构建与部署

- 前端：
  - 构建：`cd frontend && npm run build`
  - 部署：将 `dist/` 静态资源托管至任意静态服务器，或与后端同域部署。
- 后端：
  - 生产建议使用 WSGI（如 gunicorn）+ 反向代理（Nginx）。
  - 设置强随机 `JWT_SECRET_KEY`，并切换到持久化数据库（如 PostgreSQL/MySQL）。

### ngrok 临时分享

开发阶段若要通过 ngrok 分享：

1) 前端允许域名：编辑 `frontend/vite.config.js` 增加
```js
server: {
  host: true,
  port: 5173,
  allowedHosts: [/\.ngrok-free\.app$/],
  // 或指定你的域名：
  // allowedHosts: ['你的子域.ngrok-free.app']
}
```
2) 后端 CORS 允许 ngrok：`backend/app.py` 中已允许 `https://*.ngrok-free.app`。
3) 启动 ngrok：`ngrok http 5173`，使用生成的 `https://<sub>.ngrok-free.app` 访问。

## 后续优化建议

- UI：暗色模式、响应式适配、文章卡片化与骨架屏。
- 功能：文章搜索、分页、点赞、富文本编辑与草稿箱。
- 安全：更细粒度的权限控制、CSRF 防护（对非 JWT 场景）、速率限制。

## 许可

本项目用于学习与演示，欢迎自由修改与扩展。
