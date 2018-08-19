import Vue from 'vue'

import axios from 'axios'
import VueAxios from 'vue-axios'
import Vuex from 'vuex'

import App from './App'
import router from './router'

import BootstrapVue from 'bootstrap-vue'

Vue.use(VueAxios, axios)
Vue.use(Vuex)
Vue.use(BootstrapVue)

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

const store = new Vuex.Store({
    state: {
        set: new Set()
    },
    mutations: {
        add(state, value) {
            state.set = new Set(state.set).add(value)
        },
        delete(state, value) {
            const nSet = new Set(state.set)
            nSet.delete(value)
            state.set = nSet
        }
    }
})

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
    el: '#app',
    router,
    store,
    components: {App},
    template: '<App/>'
})
