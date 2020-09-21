import Vue from 'vue'
import Vuex from 'vuex'
import VueCookies from 'vue-cookies'

Vue.use(Vuex)
Vue.use(VueCookies)

import mapEvent from './modules/mapEvent.js'
import mypage from './modules/mypage.js'
import schedule from './modules/schedule.js'

export default new Vuex.Store({
  state: {
    positions : [],
    isLogin: !!window.$cookies.get('auth-token'),

  },
  mutations: {

  },
  actions: {
  },
  modules: {
    mypage: mypage,
    mapEvent,
    schedule,
  }
})
