import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api/grafana': {
        target: 'http://54.82.14.166:3000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api\/grafana/, ''),
      },
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
      '/grafana': {
        target: 'http://54.82.14.166:3000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/grafana/, ''),
      },
    },
  },
});
