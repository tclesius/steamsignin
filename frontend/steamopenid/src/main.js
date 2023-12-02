import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import { OpenAPI } from './client'
import router from './router.js'
import { createPinia } from 'pinia'

OpenAPI.BASE = "http://127.0.0.1:8080" // can change so should be in .env

const pinia = createPinia()
const app = createApp(App)
app.use(pinia)
app.use(router)
app.mount('#app')
