import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/pages/Home.vue'
import EventGrid from '@/pages/EventGrid.vue'
import EventGraph from '@/pages/EventGraph.vue'

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home,
    },
    {
        path: '/event',
        name: 'EventGrid',
        component: EventGrid,
    },
    {
        path: '/event/graph',
        name: 'EventGraph',
        component: EventGraph,
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router
