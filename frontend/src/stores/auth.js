// frontend/src/stores/auth.js
import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    username: localStorage.getItem('username') || '',
    avatarUrl: localStorage.getItem('avatarUrl') || '',
  }),
  actions: {
    setAuth(token, username, avatarUrl) {
      this.token = token
      this.username = username
      localStorage.setItem('token', token)
      localStorage.setItem('username', username)
      if (avatarUrl !== undefined) {
        this.avatarUrl = avatarUrl || ''
        if (avatarUrl) localStorage.setItem('avatarUrl', avatarUrl); else localStorage.removeItem('avatarUrl')
      }
    },
    setAvatar(url) {
      this.avatarUrl = url || ''
      if (url) localStorage.setItem('avatarUrl', url); else localStorage.removeItem('avatarUrl')
    },
    logout() {
      this.token = ''
      this.username = ''
      this.avatarUrl = ''
      localStorage.removeItem('token')
      localStorage.removeItem('username')
      localStorage.removeItem('avatarUrl')
    },
  },
})