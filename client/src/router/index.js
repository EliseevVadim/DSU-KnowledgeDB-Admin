import { createRouter, createWebHistory } from 'vue-router'
import {tr} from "vuetify/locale";

const routes = [
    {
        path: '/',
        name: 'home',
        component: () => import('../views/MainAppPageView.vue')
    },
    {
        path: '/login',
        name: 'login',
        component: () => import('../views/LoginView.vue')
    },
    {
        path: '/register',
        name: 'register',
        component: () => import('../views/RegistrationView.vue')
    }
]

const router = createRouter({
        history: createWebHistory(),
        routes
    }
)

export default router