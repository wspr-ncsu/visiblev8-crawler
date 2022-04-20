import {createRouter, createWebHistory} from 'vue-router'

import Index from '@/views/Index.vue'
import Result from '@/views/Result.vue'
import About from '@/views/About.vue'
import History from '@/views/History.vue'
import PageNotFound from '@/views/PageNotFound.vue'

// add router

const routes = [
    {
      path: '/', 
      name: 'Index', 
      component: Index
    },
    {
      path: '/about', 
      name: 'About',  
      component: About
    },
    {
      path: '/result/:id',
      name: 'Result', 
      component: Result
    },
    {
      path: '/history', 
      name: 'History', 
      component: History
    },
    {
      path: '/:catchAll(.*)*',
      name: "PageNotFound",
      component: PageNotFound,
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