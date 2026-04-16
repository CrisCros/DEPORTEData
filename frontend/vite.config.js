import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
export default defineConfig({
    plugins: [react()],
    server: {
        proxy: {
            '/api/grafana': {
                target: 'http://35.169.239.40:3000',
                changeOrigin: true,
                rewrite: function (path) { return path.replace(/^\/api\/grafana/, ''); },
            },
            '/api': {
                target: 'http://localhost:8000',
                changeOrigin: true,
                rewrite: function (path) { return path.replace(/^\/api/, ''); },
            },
            '/grafana': {
                target: 'http://35.169.239.40:3000',
                changeOrigin: true,
                rewrite: function (path) { return path.replace(/^\/grafana/, ''); },
            },
        },
    },
});
