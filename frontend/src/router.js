    import Vue from 'vue'
import VueRouter from 'vue-router'
Vue.use(VueRouter)

function getPropsForRoute(route) {
    return { name: route.path }
}

export default new VueRouter({
    mode: "history",
    base: "/vue/",
    routes: [
        {
            path: "/console",
            redirect: "console/dashboard",
            component: () => import("./views/Console"),
            children: [
                {
                    path: "dashboard",
                    component: () => import("./views/components/Dashboard"),
                    props: getPropsForRoute
                },
                {
                    path: "inspector",
                    component: () => import("./views/components/NanotaskInspector"),
                    props: getPropsForRoute
                },
                {
                    path: "events",
                    component: () => import("./views/components/Operation"),
                    props: getPropsForRoute
                },
                {
                    path: "flow",
                    component: () => import("./views/components/TaskFlowDesigner"),
                    props: getPropsForRoute
                },
                {
                    path: "answers",
                    component: () => import("./views/components/AnswerViewer"),
                    props: getPropsForRoute
                }
            ]
        },
        {
            path: "/private-prod/:projectName",
            component: () => import("./views/private-prod/Main.vue"),
            props: true
        },
        {
            path: "/private-prod-login",
            component: () => import("./views/PrivateProdLogin.vue"),
            props: true
        },
        {
            path: "/vuep",
            component: () => import("./views/Vuep")
        }
    ]
})
