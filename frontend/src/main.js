import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

import CoreuiVue from '@coreui/vue'
import CIcon from '@coreui/icons-vue'
import { iconsSet as icons } from '@/assets/icons'
import { CirclesToRhombusesSpinner } from 'epic-spinners'

import {
  Chart,
  LineController,
  LineElement,
  PointElement,
  LinearScale,
  LogarithmicScale,
  CategoryScale,
  Title,
  BarElement,
  Legend,
  Tooltip,
} from 'chart.js'
Chart.register(
  LineController,
  LineElement,
  BarElement,
  PointElement,
  LinearScale,
  CategoryScale,
  LogarithmicScale,
  Title,
  Legend,
  Tooltip,
)

const app = createApp(App)

router.beforeEach((to, from, next) => {
  console.log(from, to)
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    if (!store.getters.loggedIn) {
      console.log('Not logged in, redirect')
      next({ name: 'Login', query: { next: to.fullPath } })
    } else {
      next()
    }
  } else if (to.matched.some((record) => record.meta.requiresNotAuth)) {
    if (store.getters.loggedIn) {
      next({ name: 'Blog' })
    } else {
      next()
    }
  } else {
    next()
  }
})

app.use(store)
app.use(router)
app.use(CoreuiVue)
app.provide('icons', icons)
app.component('CIcon', CIcon)
app.component('CirclesToRhombusesSpinner', CirclesToRhombusesSpinner)
app.mount('#app')
