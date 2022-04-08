import { createApp } from 'vue'
import router from './router'

import App from './App.vue'



// add normalize.css
import 'normalize.css'
import '@/assets/styles/style.css'


createApp(App).use(router).mount('#app')



