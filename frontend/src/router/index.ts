import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
      meta: { public: true }
    },
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomeView.vue')
    },
    {
      path: '/outline',
      name: 'outline',
      component: () => import('../views/OutlineView.vue')
    },
    {
      path: '/generate',
      name: 'generate',
      component: () => import('../views/GenerateView.vue')
    },
    {
      path: '/result',
      name: 'result',
      component: () => import('../views/ResultView.vue')
    },
    {
      path: '/history',
      name: 'history',
      component: () => import('../views/HistoryView.vue')
    },
    {
      path: '/history/:id',
      name: 'history-detail',
      component: () => import('../views/HistoryView.vue')
    }
  ]
})

router.beforeEach(async (to, _from, next) => {
  if (to.meta.public) {
    next()
    return
  }

  const authStore = useAuthStore()

  if (!authStore.token) {
    next('/login')
    return
  }

  if (!authStore.isAuthenticated && !authStore.isValidating) {
    const valid = await authStore.validateToken()
    if (!valid) {
      next('/login')
      return
    }
  }

  next()
})

export default router
