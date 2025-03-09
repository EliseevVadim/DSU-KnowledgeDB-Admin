import { createRouter, createWebHistory } from 'vue-router'

const routes = [
    {
        path: '/',
        redirect: '/dashboard',
        name: 'home',
        meta: {
            title: 'DonSU Knowledge Database Admin'
        }
    },
    {
        path: '/login',
        name: 'login',
        meta: {
            title: 'Авторизация'
        },
        component: () => import('../views/LoginView.vue')
    },
    {
        path: '/register',
        name: 'register',
        meta: {
            title: 'Регистрация'
        },
        component: () => import('../views/RegistrationView.vue')
    },
    {
        path: '/dashboard',
        name: 'panel',
        meta: {
            title: 'Главная'
        },
        component: () => import('../views/MainAppPageView.vue'),
        children: [
            {
                path: '/documents',
                name: 'documents',
                meta: {
                    title: 'Документы'
                },
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

router.beforeEach((to, from, next) => {
    document.title = to.meta.title || 'DonSU Knowledge Database Admin';
    next();
});

export default router