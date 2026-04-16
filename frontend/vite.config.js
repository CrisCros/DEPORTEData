import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';
export default defineConfig(function (_a) {
    var mode = _a.mode;
    var env = loadEnv(mode, '.', '');
    var devApiTarget = env.VITE_DEV_API_TARGET || 'http://localhost:8000';
    return {
        plugins: [react()],
        server: {
            proxy: {
                '/api/grafana': {
                    target: 'http://35.169.239.40:3000',
                    changeOrigin: true,
                    rewrite: function (path) { return path.replace(/^\/api\/grafana/, ''); },
                },
                '/api': {
                    target: devApiTarget,
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
    };
});
