import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import HomeView from '@/views/HomeView.vue'
import NhmallView from '@/views/NhmallView.vue'
import MartView from '@/views/MartView.vue'
import LoginView from '@/views/LoginView.vue'
import SignupView from '@/views/SignupView.vue'
import SavingAddView from '@/views/SavingAddView.vue'
import SavingsList from '@/components/savings/SavingsList.vue'
import OptionsList from '@/components/savings/OptionsList.vue'
import RecommendView from '@/views/RecommendView.vue'
import QuestionList from '@/components/articles/QuestionList.vue'
import QuestionDetail from '@/components/articles/QuestionDetail.vue'
import CreateQuestion from '@/components/articles/CreateQuestion.vue'

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
      path: '/accounts/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/accounts/signup',
      name: 'signup',
      component: SignupView,
    },
    {
      path: '/savings/add',
      name: 'savingadd',
      component: SavingAddView,
      props: true,
      meta: { requiresAuth: true },
    },
    {
      path: "/savings/list",
      name: "SavingsList",
      component: SavingsList,
    },
    {
      path: "/savings/list/:id/options",
      name: "OptionsList",
      component: OptionsList,
      props: (route) => ({ id: Number(route.params.id) }), // 숫자로 변환
    },    
    {
      path: '/savings/recommend',
      name: 'recommend',
      component: RecommendView,
      props: true,
      meta: { requiresAuth: true },
    },
    {
      path: "/articles/",
      component : QuestionList,
    },
    {
      path: '/articles/question/:id',
      component: QuestionDetail,
      props: true,
    },
    {
      path: '/articles/create-question/',
      component: CreateQuestion,
    },
  ],
})

// 전역 네비게이션 가드
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore(); // Pinia 스토어 가져오기

  if (to.meta.requiresAuth && !authStore.isLoggedIn) {
    // 로그인이 필요한 페이지에 접근 시
    alert("로그인이 필요합니다. 로그인 페이지로 이용합니다."); // 알림 창 표시
    next({
      path: "/accounts/login", // 로그인 페이지로 이동
      query: { redirect: to.fullPath }, // 로그인 후 돌아갈 경로 저장
    });
  } else {
    // 로그인 상태이거나 로그인 불필요한 페이지로 이동
    next();
  }
});

export default router;

