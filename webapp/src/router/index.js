import {createRouter, createWebHistory} from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SignupView from '../views/SignupView.vue'
import CallbackView from '../views/CallbackView.vue'
import LoginView from '../views/LoginView.vue'
import AboutView from '../views/AboutView.vue'
import {useAuth0} from "@auth0/auth0-vue";
import auth from "@/ultils/auth";
import NotFoundView from "@/views/NotFoundView.vue";
import MaintenanceView from "@/views/MaintenanceView.vue";
import CommingSoonView from "@/views/CommingSoonView.vue";

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'home',
            // component: HomeView
            component: CommingSoonView
        },
        {
            path: '/beta',
            name: 'home-beta',
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
        {
            path: '/maintenance',
            name: 'maintenance',
            component: MaintenanceView
        },
        // Add a wildcard route for 404 page
        {
            path: '/:catchAll(.*)',
            component: NotFoundView,
        },
    ]
});

router.beforeEach(async (to, from, next) => {
    // Send a pageview event to Google Analytics for each route change
    if (window.gtag) {
        window.gtag('config', 'YOUR_GA_TRACKING_ID', {page_path: to.path});
    }

    if (to.matched.some((record) => record.meta.requiresAuth)) {
        // Route requires authentication, check if the user is logged in
        // const auth0 = useAuth0()
        // await auth0.checkSession();
        // await auth0.getAccessTokenSilently()
        // await auth.authenticate()
        if (await auth.authenticate()) {
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
