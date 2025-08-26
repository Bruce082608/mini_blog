import { createRouter, createWebHistory } from 'vue-router'
import Home from '../pages/Home.vue'
import Article from '../pages/article.vue'
import Login from '../pages/Login.vue'
import Register from '../pages/Register.vue'
import Publish from '../pages/Publish.vue'
import Me from '../pages/Me.vue'
import EditArticle from '../pages/EditArticle.vue'

const routes = [
  { path: '/', name: 'home', component: Home },
  { path: '/article/:id', name: 'article', component: Article },
  { path: '/article/:id/edit', name: 'article-edit', component: EditArticle },
  { path: '/login', name: 'login', component: Login },
  { path: '/register', name: 'register', component: Register },
  { path: '/publish', name: 'publish', component: Publish },
  { path: '/me', name: 'me', component: Me },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router