import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// Custom plugin to log file changes to the terminal for better visibility in Docker
const terminalLogger = {
  name: 'terminal-logger',
  handleHotUpdate({ file }) {
    console.log(`\x1b[32m[vite] File changed: \x1b[0m${file.split('/').pop()}`);
  }
}

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss(), terminalLogger],
  server: {
    host: '0.0.0.0',
    watch: {
      usePolling: true,
    },
    hmr: {
      host: 'localhost',
    },
  },
})
