import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  base: './',
  // Each volume's dataset is its own lazily loaded chunk of 0.5-0.7 MB; only one loads at a time.
  build: { chunkSizeWarningLimit: 800 },
})
