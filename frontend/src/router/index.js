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
                component: () => import("@/components/pages/Console/TaskFlow"),
            },
            {
                path: "platform/mturk",
                redirect: "platform/mturk/top",
                component: () => import("@/components/pages/Console/Platforms/MTurk"),
                children: [
                    {
                        path: "top",
                        component: () => import("@/components/pages/Console/Platforms/MTurk/Top"),
                    },
                    {
                        path: "hit",
                        component: () => import("@/components/pages/Console/Platforms/MTurk/HIT"),
                    },
                    {
                        path: "hit/create",
                        component: () => import("@/components/pages/Console/Platforms/MTurk/HIT/Create"),
                    },
                    {
                        path: "qual",
                        component: () => import("@/components/pages/Console/Platforms/MTurk/Qualification"),
                    },
                    {
                        path: "worker",
                        component: () => import("@/components/pages/Console/Platforms/MTurk/Worker"),
                    },
                    {
                        path: "assignment",
                        component: () => import("@/components/pages/Console/Platforms/MTurk/Assignment"),
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
        props: true,
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
