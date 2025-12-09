import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [react()],
    server: {
        host: true, // Necessário para Docker
        proxy: {
            // Redireciona chamadas /predict e /graphql para o backend Python
            '/predict': process.env.API_URL || 'http://127.0.0.1:8000',
            '/graphql': process.env.API_URL || 'http://127.0.0.1:8000',
        }
    }
})
