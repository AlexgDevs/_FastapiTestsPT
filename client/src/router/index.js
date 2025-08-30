import { createRouter, createWebHistory } from 'vue-router'

import Users from '../components/Users.vue'
import Test from '../components/Test.vue'

const routes = [
    {path: '/users', name: 'Users', component: Users  },
    {path: '/test', name:'Test', component: Test}
]

const router = createRouter({
    history: createWebHistory(),
    routes: routes  // ← именно так!
})

export default router 