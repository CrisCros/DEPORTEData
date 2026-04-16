import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, '.', '');
  const devApiTarget = env.VITE_DEV_API_TARGET || 'http://localhost:8000';
  return {
    plugins: [react()],
    server: {
      proxy: {
        '/api/grafana': {
          target: 'http://35.169.239.40:3000',
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api\/grafana/, ''),
        },
        '/api': {
          target: devApiTarget,
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, ''),
        },
        '/grafana': {
          target: 'http://35.169.239.40:3000',
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/grafana/, ''),
        },
      },
    },
  };
});
