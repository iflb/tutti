import Vue from 'vue'
import VueRouter from 'vue-router'
Vue.use(VueRouter)

function getPropsForRoute(route) {
    return { name: route.path }
}

export default new VueRouter({
    mode: "history",
    base: process.env.BASE_URL,
    //base: "/vue-dev/",
    routes: [
        {
            path: "/console",
            redirect: "console/dashboard",
            component: () => import("./views/Console/Main"),
            children: [
                {
                    path: "dashboard",
                    component: () => import("./views/Console/Dashboard"),
                    props: getPropsForRoute
                },
                {
                    path: "template",
                    component: () => import("./views/Console/Template"),
                    props: getPropsForRoute
                },
                {
                    path: "flow",
                    component: () => import("./views/Console/TaskFlow/Main"),
                    props: getPropsForRoute
                },
                {
                    path: "platform/mturk-new",
                    component: () => import("./views/Console/Platforms/MTurk/MainNew")
                },
                {
                    path: "platform/mturk",
                    component: () => import("./views/Console/Platforms/MTurk/Main"),
                    props: getPropsForRoute
                },
                {
                    path: "platform/mturk/hit/",
                    component: () => import("./views/Console/Platforms/MTurk/HIT/Main"),
                    props: getPropsForRoute
                },
                {
                    path: "platform/mturk/hit/create/",
                    component: () => import("./views/Console/Platforms/MTurk/HIT/Create"),
                    props: getPropsForRoute
                },
                {
                    path: "platform/mturk/qual/",
                    component: () => import("./views/Console/Platforms/MTurk/Qualification/Main"),
                    props: getPropsForRoute
                },
                {
                    path: "answer",
                    component: () => import("./views/Console/Answer"),
                    props: getPropsForRoute
                },
                {
                    path: "event",
                    component: () => import("./views/Console/Event"),
                    props: getPropsForRoute
                },
            ]
        },
        {
            path: "/private-prod/:projectName",
            component: () => import("./views/PrivateProd/Main.vue"),
            props: true,
        },
        {
            path: "/private-prod/:projectName/preview",
            component: () => import("./views/PrivateProd/Preview.vue"),
        },
        {
            path: "/private-prod-login",
            component: () => import("./views/PrivateProdLogin.vue"),
            props: true
        },
        //{
        //    path: "/vuep",
        //    component: () => import("./views/Vuep")
        //}
    ]
})
