import react from '@vitejs/plugin-react'
import { loadEnv } from 'vite'
import { defineConfig } from 'vitest/config'

// HU-072 — la SPA llama a `/api` en el mismo origen. En desarrollo, Vite reenvía ese
// prefijo a la API local y lo elimina antes de llegar a FastAPI (`/predict`).
// `VITE_API_PROXY` permite apuntar a otro host o puerto.
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, '.', '')

  return {
    plugins: [react()],
    server: {
      port: 5173,
      strictPort: true,
      proxy: {
        '/api': {
          target: env.VITE_API_PROXY || 'http://localhost:8000',
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, ''),
        },
      },
    },
    build: {
      outDir: 'dist',
      sourcemap: true,
    },
    test: {
      environment: 'jsdom',
      globals: true,
      setupFiles: './src/setupTests.ts',
      css: false,
      restoreMocks: true,
    },
  }
})
