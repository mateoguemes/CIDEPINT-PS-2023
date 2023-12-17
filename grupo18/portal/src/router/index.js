import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import RequestForm from '../views/RequestForm.vue'
import Request from '../views/Requests.vue'
import Notes from '../views/Notes.vue'
import NoteForm from '../views/NoteForm.vue'
import RequestDetail from '../views/RequestDetail.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/Aa.vue')
    },
    {
      path: '/request/:serviceId',
      name: 'request',
      component: RequestForm
    },
    {
      path: '/myRequests',
      name: 'myRequests',
      component: Request
    },
    {
      path: '/notes/:requestId',
      name: 'notes',
      component: Notes
    },
    {
      path: '/submitNotes/:requestId',
      name: 'noteForm',
      component: NoteForm
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/Login.vue'),
    },
    {path: '/service-detail/:id',
      name: 'service-detail',
      component: () => import('../views/view_servicedetail.vue'),
      props: true,  // Esto permite pasar el parámetro como propiedad al componente}
    },
    {
      path: '/request-detail/:requestId',
      name: 'request-detail',
      component: () => import('../views/RequestDetail.vue'),
    },
    {
      path: '/statistics',
      name: 'Statistics',
      component: () => import('../views/Statistics.vue'),
    },
    {
      path: '/services',
      name: 'services',
      component: () => import('../views/Services.vue'),
    } 
  ]
})

export default router
