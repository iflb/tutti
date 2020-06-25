import Vue from 'vue'
import App from './App.vue'
import store from './store'
import router from './router'
import vuetify from '@/plugins/vuetify'
import '@mdi/font/css/materialdesignicons.css'

Vue.config.productionTip = false

new Vue({
    vuetify,
    store,
    router,
    render: h => h(App),
}).$mount('#app')
