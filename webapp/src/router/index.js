import {createRouter, createWebHistory} from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SignupView from '../views/SignupView.vue'
import CallbackView from '../views/CallbackView.vue'
import AboutView from '../views/AboutView.vue'
import auth from "@/ultils/auth";
import NotFoundView from "@/views/NotFoundView.vue";
import MaintenanceView from "@/views/MaintenanceView.vue";
import CommingSoonView from "@/views/CommingSoonView.vue";
import LogoutView from "@/views/LogoutView.vue";
import LoginView from "@/view_share/LoginView.vue";

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
            path: '/logout',
            name: 'logout',
            component: LogoutView
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
        // Admin routes
        {
            path: '/admin/login',
            name: 'admin-login',
            component: LoginView
        },
        {
            path: '/admin',
            name: 'admin-home',
            component: () => import('../admin/views/AdminHome.vue'),
            meta: {
                requiresAuth: true,
            },
        },
        {
            path: '/admin/urls',
            name: 'admin-urls',
            component: () => import('../admin/views/AdminURLs.vue'),
            meta: {
                requiresAuth: true,
            },
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
        window.gtag('config', 'G-2JR8BXX3D3', {page_path: to.path});
    }

    if (to.matched.some((record) => record.meta.requiresAuth)) {
        // Route requires authentication, check if the user is logged in
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
