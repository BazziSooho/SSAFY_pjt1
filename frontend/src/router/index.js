import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import NhmallView from '@/views/NhmallView.vue'
import MartView from '@/views/MartView.vue'
import LoginView from '@/views/LoginView.vue'
import SignupView from '@/views/SignupView.vue'
// import SupportView from '@/views/SupportView.vue'
// import ProfileView from '@/views/ProfileView.vue'
import EventView from '@/views/EventView.vue'
// import MapView from '@/views/MapView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/nhmall',
      name: 'nhmall',
      component: NhmallView,
    },
    {
      path: '/mart',
      name: 'mart',
      component: MartView,
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/event',
      name: 'event',
      component: EventView,
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignupView,
    },
    // {
    //   path: '/support',
    //   name: 'support',
    //   component: SupportView,
    // },
  ],
})

export default router
