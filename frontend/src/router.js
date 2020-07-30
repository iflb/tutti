import Vue from 'vue'
import VueRouter from 'vue-router'

import Console from './views/Console'
import Dashboard from './views/components/Dashboard'
import NanotaskInspector from './views/components/NanotaskInspector'
import Operation from './views/components/Operation'

import PrivateProd from './views/PrivateProd'

Vue.use(VueRouter)

const router = new VueRouter({
    mode: "history",
    base: "/vue/",
    routes: [
        {
            path: "/console",
            redirect: "/console/dashboard",
            component: Console,
            children: [
                { path: "dashboard", component: Dashboard },
                { path: "inspector", component: NanotaskInspector },
                { path: "events", component: Operation }
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
