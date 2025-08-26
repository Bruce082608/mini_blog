import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    host: true,
    port: 5173,
    allowedHosts: [/\.ngrok-free\.app$/],
    allowedHosts: ['80cad776658e.ngrok-free.app']  //用ngrok访问的示例（去掉https://）
  },
})
