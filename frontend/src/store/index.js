import { createStore } from 'vuex'
import jwtDecode from 'jwt-decode'

import {
  AUTH_BLACKLIST_TOKEN_API,
  AUTH_GET_TOKEN_API,
  AUTH_REFRESH_TOKEN_API,
  fetch_auth_json,
} from '@/common/api_endpoints'

const authenticationModule = {
  state: {
    accessToken: localStorage.getItem('access_token') || null,
    refreshToken: localStorage.getItem('refresh_token') || null,
  },
  mutations: {
    updateLocalStorage(state, { access, refresh }) {
      state.accessToken = access
      state.refreshToken = refresh
      localStorage.setItem('access_token', access)
      localStorage.setItem('refresh_token', refresh)
    },
    updateAccess(state, access) {
      state.accessToken = access
      localStorage.setItem('access_token', access)
    },
    destroyToken(state) {
      state.accessToken = null
      state.refreshToken = null
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
    },
  },
  actions: {
    async refreshToken(context) {
      if (context.state.refreshToken) {
        const res = await fetch_auth_json(AUTH_REFRESH_TOKEN_API, 'POST', {
          refresh: context.state.refreshToken,
        })
        const data = await res.json()
        if (data.access) {
          context.commit('updateAccess', data.access)
        }
        return data.access !== undefined
      } else {
        return false
      }
    },
    async loginUser(context, credentials) {
      const res = await fetch_auth_json(AUTH_GET_TOKEN_API, 'POST', {
        username: credentials.username,
        password: credentials.password,
        recaptcha: credentials.recaptcha,
      })
      let wrong_cred = res.status !== 200
      const data = await res.json()
      console.log('Rec data', data)
      if (data.access && data.refresh) {
        context.commit('updateLocalStorage', {
          access: data.access,
          refresh: data.refresh,
        })
      }
      return wrong_cred
    },
    async logoutUser(context) {
      await fetch_auth_json(AUTH_BLACKLIST_TOKEN_API, 'POST', {
        refresh: context.state.refreshToken,
      })
      context.commit('destroyToken')
    },
    async getAuthHeader(context) {
      const jwtPayload = jwtDecode(context.state.accessToken)
      if (jwtPayload.exp < Date.now() / 1000) {
        await context.dispatch('refreshToken')
      }
      return `Bearer ${context.state.accessToken}`
    },
  },
  getters: {
    loggedIn(state) {
      return state.accessToken != null
    },
  },
}

export default createStore({
  state: {
    sidebarVisible: '',
    sidebarUnfoldable: false,
  },
  mutations: {
    toggleSidebar(state) {
      state.sidebarVisible = !state.sidebarVisible
      window.dispatchEvent(new Event('resize'))
    },
    toggleUnfoldable(state) {
      state.sidebarUnfoldable = !state.sidebarUnfoldable
      window.dispatchEvent(new Event('resize'))
    },
    updateSidebarVisible(state, payload) {
      state.sidebarVisible = payload.value
      window.dispatchEvent(new Event('resize'))
    },
  },
  actions: {},
  modules: { authenticationModule },
})
