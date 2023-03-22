import { h, resolveComponent } from 'vue'
import { createRouter, createWebHashHistory } from 'vue-router'

import DefaultLayout from '@/layouts/DefaultLayout'
// import CardLayout from '@/layouts/CardLayout'
import EmptyLayout from '@/layouts/EmptyLayout'

const routes = [
  {
    path: '/',
    name: '',
    component: DefaultLayout,
    redirect: '/browse',
    children: [
      {
        path: '/browse',
        name: 'Dashboard',
        redirect: '/browse/main/',
        component: EmptyLayout,
        meta: {
          requiresAuth: true,
        },
        children: [
          {
            path: 'main/',
            name: 'Main',
            component: () => import('@/views/sound_sorting/Main.vue'),
            meta: {
              requiresAuth: false,
            },
          },
          {
            path: 'sound_sorting/',
            name: 'Sound Sorting',
            component: () =>
              import('@/views/sound_sorting/GameSoundExplorer.vue'),
          },
          {
            path: 'bounties/',
            name: 'Bounties',
            component: () => import('@/views/sound_sorting/Bounties.vue'),
          },
        ],
      },
    ],
  },
  {
    path: '/pages',
    redirect: '/pages/404',
    name: 'Pages',
    component: {
      render() {
        return h(resolveComponent('router-view'))
      },
    },
    children: [
      {
        path: '404',
        name: 'Page404',
        component: () => import('@/views/pages/Page404'),
      },
      {
        path: 'login',
        name: 'Login',
        meta: {
          requiresNotAuth: true,
        },
        component: () => import('@/views/pages/Login'),
      },
      {
        path: 'signup',
        name: 'Signup',
        meta: {
          requiresNotAuth: true,
        },
        component: () => import('@/views/pages/Signup.vue'),
      },
      {
        path: 'logout',
        name: 'Logout',
        component: () => import('@/views/pages/Logout'),
      },
    ],
  },
  {
    path: '/:catchAll(.*)',
    redirect: '/pages/404',
  },
]

const router = createRouter({
  history: createWebHashHistory(process.env.BASE_URL),
  routes,
  scrollBehavior() {
    // always scroll to top
    return { top: 0 }
  },
})

export default router
