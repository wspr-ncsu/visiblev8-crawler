import {createRouter, createWebHistory} from 'vue-router'

import Index from '@/views/Index.vue'
import Result from '@/components/Result.vue'
import About from '@/views/About.vue'
import History from '@/views/History.vue'

// add router

const routes = [
    {
      path: '/', 
      name: 'Index', 
      component: Index
    },
    {
      path: '/about', 
      name: 'about',  
      component: About
    },
    {
      path: '/result', 
      name: 'result', 
      component: Result
    },
    {
      path: '/history', 
      name: 'history', 
      component: History
    },
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