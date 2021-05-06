import Vue from 'vue'
import VueRouter from 'vue-router'
Vue.use(VueRouter)

const routes = [
    {
        path: "/",
        redirect: "console"
    },
    {
        path: "/console",
        redirect: "console/dashboard",
        component: () => import("@/views/Console"),
        children: [
            {
                path: "dashboard",
                component: () => import("@/components/pages/ConsoleDashboard"),
            },
            {
                path: "template",
                component: () => import("@/components/pages/ConsoleTemplate"),
            },
            {
                path: "flow",
                component: () => import("@/views/ConsoleComponents/TaskFlow/Main"),
            },
            {
                path: "platform/mturk",
                redirect: "platform/mturk/top",
                component: () => import("@/views/ConsoleComponents/Platforms/MTurk/Main"),
                children: [
                    {
                        path: "top",
                        component: () => import("@/views/ConsoleComponents/Platforms/MTurk/Top"),
                    },
                    {
                        path: "hit",
                        component: () => import("@/views/ConsoleComponents/Platforms/MTurk/HIT/Main"),
                    },
                    {
                        path: "hit/create",
                        component: () => import("@/views/ConsoleComponents/Platforms/MTurk/HIT/Create"),
                    },
                    {
                        path: "qual",
                        component: () => import("@/views/ConsoleComponents/Platforms/MTurk/Qualification/Main"),
                    },
                    {
                        path: "worker",
                        component: () => import("@/views/ConsoleComponents/Platforms/MTurk/Worker/Main"),
                    },
                    {
                        path: "assignment",
                        component: () => import("@/views/ConsoleComponents/Platforms/MTurk/Assignment/Main"),
                    },
                ]
            },
            {
                path: "response",
                component: () => import("@/components/pages/ConsoleResponse"),
            },
            {
                path: "event",
                component: () => import("@/components/pages/ConsoleEvent"),
            },
        ]
    },
    {
        path: "/private-prod/:projectName",
        component: () => import("@/views/PrivateProd/Main.vue"),
    },
    {
        path: "/private-prod-login",
        component: () => import("@/views/PrivateProdLogin.vue"),
    },
]

const router = new VueRouter({
    mode: "history",
    base: process.env.BASE_URL,
    //base: "/vue-dev/",
    routes 
})

export default router
