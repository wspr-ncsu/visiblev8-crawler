import { createApp } from 'vue'
import {createRouter, createWebHistory} from 'vue-router'
import App from './App.vue'
import Index from '@/components/Index.vue'
import Result from '@/components/Result.vue'
import About from '@/components/About.vue'


// add normalize.css
import 'normalize.css'
import '@/assets/styles/style.css'


// add router

const routes = createRouter({
    history: createWebHistory(),
    routes: [
        {path: '/', name: 'Index', component: Index},
        {path: '/about', name: 'About', component: About},
        {path: '/result', name: 'Result', component: Result},
    ]
  })



createApp(App).mount('#app')



