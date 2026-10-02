import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// ビルド成果物は Spring Boot の静的リソース (target/classes/static) に直接出力し、WAR に同梱する
export default defineConfig({
  plugins: [react()],
  build: {
    outDir: '../target/classes/static',
    emptyOutDir: true,
  },
  // npm run dev 時は API を Tomcat (8080) にプロキシ
  server: {
    port: 5173,
    proxy: {
      '/api': 'http://localhost:8080',
    },
  },
});
