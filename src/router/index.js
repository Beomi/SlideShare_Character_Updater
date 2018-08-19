import Vue from 'vue'
import Router from 'vue-router'

import Uploader from '@/components/Uploader'

Vue.use(Router)

export default new Router({
    routes: [
        {
            path: '/',
            alias: '/upload',
            name: 'Uploader',
            component: Uploader
        },
    ]
})
