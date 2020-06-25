import Vue from 'vue'
import VueRouter from 'vue-router'

import Console from './views/Console'
import Dashboard from './views/components/Dashboard'
import NanotaskTester from './views/components/NanotaskTester'
import Operation from './views/components/Operation'

Vue.use(VueRouter)

const router = new VueRouter({
    mode: "history",
    base: "/vue/",
    routes: [
        {
            path: "/operation",
            component: Operation,
        },
        {
            path: "/console",
            redirect: "/console/dashboard",
            component: Console,
            children: [
                { path: "dashboard", component: Dashboard },
                { path: "tester", component: NanotaskTester },
                { path: "events", component: Operation }
            ]
        },
    ]
})

export default router
