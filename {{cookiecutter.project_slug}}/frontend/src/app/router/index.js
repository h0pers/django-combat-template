import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/app/views/HomeView.vue'),
  },
]

const router = createRouter({
  history: createWebHistory('/app/'),
  routes,
})

export default router
