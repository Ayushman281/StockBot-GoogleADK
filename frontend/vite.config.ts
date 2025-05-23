import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// Add explicit type for Node.js process
declare const process: {
  env: {
    NODE_ENV?: string;
    REACT_APP_USE_MOCK_DATA?: string;
  }
};

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  optimizeDeps: {
    exclude: ['lucide-react'],
  },
  server: {
    proxy: {
      // Proxy API requests to backend during development
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  },
  build: {
    // Ensure proper static asset handling
    outDir: 'dist',
    assetsDir: 'assets',
    sourcemap: false,
    // Fix module loading issues
    rollupOptions: {
      output: {
        manualChunks: undefined,
      }
    }
  },
  define: {
    // Define environment variables to be used in the app
    'process.env': {
      NODE_ENV: JSON.stringify(process.env.NODE_ENV),
      REACT_APP_USE_MOCK_DATA: JSON.stringify(process.env.REACT_APP_USE_MOCK_DATA || 'false')
    }
  }
});
