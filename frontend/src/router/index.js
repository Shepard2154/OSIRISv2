import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('../views/Home.vue'),
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('../views/Login.vue'),
  },
  {
    path: '/search',
    name: 'search',
    component: () => import('../views/Search.vue'),
  },
  {
    path: '/negative',
    name: 'negative',
    component: () => import('../views/Negative.vue'),
  },
  {
    path: '/reasons',
    name: 'reasons',
    component: () => import('../views/Reasons.vue'),
  },
  {
    path: '/geofencing',
    name: 'geofencing',
    component: () => import('../views/Geofencing.vue'),
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
