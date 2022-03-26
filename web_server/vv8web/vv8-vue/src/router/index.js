import {createRouter, createWebHistory} from 'vue-router'

import Index from '@/components/Index.vue'
import Result from '@/components/Result.vue'
import About from '@/components/About.vue'
import History from '@/components/History.vue'

// add router

const routes = [
    {path: '/', name: 'Index', component: Index},
    {path: '/about', name: 'About', component: About},
    {path: '/result', name: 'Result', component: Result},
    {path: '/history', name: 'History', component: History},


]


const router = createRouter({
    history: createWebHistory(),
    routes
  })


// routing guard
router.beforeEach( (to, from) => {
  console.log(to, from)
  console.log(to.path, from.path)
  return true
})
export default router