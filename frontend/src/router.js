import Vue from 'vue'
import VueRouter from 'vue-router'

import Console from './views/Console'
import Dashboard from './views/components/Dashboard'
import NanotaskInspector from './views/components/NanotaskInspector'
import Operation from './views/components/Operation'

import PrivateProd from './views/PrivateProd'

Vue.use(VueRouter)

function getPropsForRoute(route) {
    return { name: route.path }
}

const router = new VueRouter({
    mode: "history",
    base: "/vue/",
    routes: [
        {
            path: "/console",
            redirect: "/console/dashboard",
            component: Console,
            props: getPropsForRoute,
            children: [
                { path: "dashboard", component: Dashboard, props: getPropsForRoute },
                { path: "inspector", component: NanotaskInspector, props: getPropsForRoute },
                { path: "events", component: Operation, props: getPropsForRoute }
            ]
        },
        {
            path: "/private-prod/:projectName",
            component: PrivateProd,
            props: true
        }
    ]
})

export default router
