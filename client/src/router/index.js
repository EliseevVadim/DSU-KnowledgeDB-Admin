import { createRouter, createWebHistory } from 'vue-router'
import {tr} from "vuetify/locale";

const routes = [
    {
        path: '/',
        redirect: '/dashboard',
        name: 'home'
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
    },
    {
        path: '/dashboard',
        name: 'panel',
        component: () => import('../views/MainAppPageView.vue'),
        children: [
            {
                path: '/documents',
                name: 'documents',
                component: () => import('../views/admin/DocumentsBoardView.vue')
            }
        ]
    }
]

const router = createRouter({
        history: createWebHistory(),
        routes
    }
)

export default router