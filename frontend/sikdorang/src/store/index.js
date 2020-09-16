import Vue from 'vue'
import Vuex from 'vuex'
import VueCookies from 'vue-cookies'

Vue.use(Vuex)
Vue.use(VueCookies)

import mapEvent from './modules/mapEvent.js'

export default new Vuex.Store({
  state: {
    positions : [],
    isLogin: !!window.$cookies.get('auth-token'),

  },
  mutations: {
    storeLogin(state, payload) {
      window.$cookies.set('auth-token', payload.token)
      state.isLogin = true
    },
  },
  actions: {
  },
  modules: {
    mapEvent,
  }
})
