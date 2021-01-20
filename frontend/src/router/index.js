import Vue from 'vue'
import VueRouter from 'vue-router'
Vue.use(VueRouter)

function getPropsForRoute(route) {
    return { name: route.path }
}

const routes = [
    {
        path: "/console",
        redirect: "console/dashboard",
        component: () => import("@/views/Console/Main"),
        children: [
            {
                path: "dashboard",
                component: () => import("@/views/Console/Dashboard"),
                props: getPropsForRoute
            },
            {
                path: "template",
                component: () => import("@/views/Console/Template"),
                props: getPropsForRoute
            },
            {
                path: "flow",
                component: () => import("@/views/Console/TaskFlow/Main"),
                props: getPropsForRoute
            },
            {
                path: "platform/mturk",
                redirect: "platform/mturk/top",
                component: () => import("@/views/Console/Platforms/MTurk/Main"),
                children: [
                    {
                        path: "top",
                        component: () => import("@/views/Console/Platforms/MTurk/Top"),
                        props: getPropsForRoute
                    },
                    {
                        path: "hit",
                        component: () => import("@/views/Console/Platforms/MTurk/HIT/Main"),
                        props: getPropsForRoute
                    },
                    {
                        path: "hit/create",
                        component: () => import("@/views/Console/Platforms/MTurk/HIT/Create"),
                        props: getPropsForRoute
                    },
                    {
                        path: "qual",
                        component: () => import("@/views/Console/Platforms/MTurk/Qualification/Main"),
                        props: getPropsForRoute
                    },
                    {
                        path: "worker",
                        component: () => import("@/views/Console/Platforms/MTurk/Worker/Main"),
                        props: getPropsForRoute
                    }
                ]
            },
            {
                path: "answer",
                component: () => import("@/views/Console/Answer"),
                props: getPropsForRoute
            },
            {
                path: "event",
                component: () => import("@/views/Console/Event"),
                props: getPropsForRoute
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
        props: true
    },
    {
        path: "/test",
        component: () => import("@/views/Test/Main.vue")
    }
]

const router = new VueRouter({
    mode: "history",
    base: process.env.BASE_URL,
    //base: "/vue-dev/",
    routes 
})

export default router
