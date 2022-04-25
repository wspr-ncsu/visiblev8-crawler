import { createApp } from 'vue'
import router from './router'
import axios from 'axios'
import App from './App.vue'

axios.defaults.withCredentials = true;
axios.defaults.baseURL = `${window.origin}/api/v1`;  // the FastAPI backend

// add normalize.css
import 'normalize.css'
import '@/assets/styles/style.css'


createApp(App).use(router).mount('#app')



