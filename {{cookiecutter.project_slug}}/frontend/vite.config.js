import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'
import { resolve } from 'path'

export default defineConfig({
  plugins: [vue(), tailwindcss()],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
    },
  },
  base: '/static/dist/',
  build: {
    outDir: resolve(__dirname, '../website/static/dist'),
    emptyOutDir: true,
    manifest: true,
    rollupOptions: {
      input: {
        app: resolve(__dirname, 'src/app/main.js'),
      },
    },
  },
  server: {
    origin: 'http://localhost:5173',
  },
})
