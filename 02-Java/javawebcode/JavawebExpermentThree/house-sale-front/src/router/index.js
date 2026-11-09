NEW_FILE_CODE
import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Index from '../views/Index.vue'

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/index',
    name: 'Index',
    component: Index
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
