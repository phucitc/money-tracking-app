import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SignupView from '../views/SignupView.vue'
import CallbackView from '../views/CallbackView.vue'
import LoginView from '../views/LoginView.vue'
import AboutView from '../views/AboutView.vue'
import store from "@/ultils/store"
import {useAuth0} from "@auth0/auth0-vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/home',
      name: 'home-alias',
      component: HomeView
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignupView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/callback',
      name: 'auth0-callback',
      component: CallbackView
    },
    {
      path: '/about',
      name: 'about',
      component: AboutView
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('../views/ProfileView.vue'),
      meta: {
        requiresAuth: true,
      },
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('../views/Dashboard.vue'),
      meta: {
        requiresAuth: true,
      },
    },
  ]
});

router.beforeEach(async (to, from, next) => {
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    // Route requires authentication, check if the user is logged in
    const auth0 = useAuth0()
    await auth0.checkSession();
    await auth0.getAccessTokenSilently()

    if (await auth0.isAuthenticated.value) {
      // User is authenticated, allow access
      next();
    } else {
      // User is not authenticated, redirect to login page or show access denied message
      next('/login'); // Replace '/login' with your desired login route
    }
  } else {
    // Route does not require authentication, allow access
    next();
  }
});

export default router
