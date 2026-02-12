import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/pages/Home.vue'
import Event from '@/pages/Event.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/event',
    name: 'Event',
    component: Event
  },
  {
    path: '/event/:year',
    name: 'EventByYear',
    component: Event,
    props: true // This passes route params as props to the component
  },
  // You can add more routes here, for example:
  // {
  //   path: '/athlete/:id',
  //   name: 'Athlete',
  //   component: () => import('@/pages/Athlete.vue'), // Lazy-load Athlete component
  //   props: true
  // }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
