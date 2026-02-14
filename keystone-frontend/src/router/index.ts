import {createRouter, createWebHistory} from "vue-router";

export const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: "/",
            redirect: "/dashboard"
        },
        {
            path: "/auth",
            component: () => import("../layouts/AuthLayout.vue"),
            meta: {requiresAuth: true},
            children: [
                {
                    path: "login",
                    name: "login",
                    component: () => import("../pages/auth/Login.vue"),
                    meta: {title: "Вход в систему Keystone Tracker"}
                },
                {
                    path: "register",
                    name: "registration",
                    component: () => import("../pages/auth/Register.vue"),
                    meta: {title: "Регистрация в системе Keystone Tracker"}
                }
            ]
        },
        {
            path: "/",
            component: () => import("../layouts/BaseLayout.vue"),
            meta: {requiresAuth: true},
            children: [
                {
                    path: "dashboard",
                    name: "home",
                    component: () => import( "../pages/Dashboard.vue"),
                    meta: {title: "Ваша статистика в Keystone Tracker"}
                }
            ]
        }
    ]
});