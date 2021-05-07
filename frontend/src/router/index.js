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
                component: () => import("@/components/pages/Console/Dashboard"),
            },
            {
                path: "template",
                component: () => import("@/components/pages/Console/Template"),
            },
            {
                path: "flow",
                component: () => import("@/views/ConsoleComponents/TaskFlow"),
            },
            {
                path: "platform/mturk",
                redirect: "platform/mturk/top",
                component: () => import("@/views/ConsoleComponents/Platforms/MTurk"),
                children: [
                    {
                        path: "top",
                        component: () => import("@/views/ConsoleComponents/Platforms/MTurk/Top"),
                    },
                    {
                        path: "hit",
                        component: () => import("@/views/ConsoleComponents/Platforms/MTurk/HIT"),
                    },
                    {
                        path: "hit/create",
                        component: () => import("@/views/ConsoleComponents/Platforms/MTurk/HIT/Create"),
                    },
                    {
                        path: "qual",
                        component: () => import("@/views/ConsoleComponents/Platforms/MTurk/Qualification"),
                    },
                    {
                        path: "worker",
                        component: () => import("@/views/ConsoleComponents/Platforms/MTurk/Worker"),
                    },
                    {
                        path: "assignment",
                        component: () => import("@/views/ConsoleComponents/Platforms/MTurk/Assignment"),
                    },
                ]
            },
            {
                path: "response",
                component: () => import("@/components/pages/Console/Response"),
            },
            {
                path: "event",
                component: () => import("@/components/pages/Console/Event"),
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
