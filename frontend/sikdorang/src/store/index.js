import Vue from 'vue'
import Vuex from 'vuex'
import VueCookies from 'vue-cookies'

Vue.use(Vuex)
Vue.use(VueCookies)

import mapEvent from './modules/mapEvent.js'
import mypage from './modules/mypage.js'
import schedule from './modules/schedule.js'
import themes from './modules/themes.js'

export default new Vuex.Store({
  state: {
    positions : [],
    isLogin: !!window.$cookies.get('auth-token'),
    SERVER_URL: 'http://j3d202.p.ssafy.io:8080/',
    LOCAL_URL: 'http://j3d202.p.ssafy.io:8181/project/sikdorang',


  },
  mutations: {

  },
  actions: {
  },
  modules: {
    mypage: mypage,
    mapEvent,
    schedule,
    themes,
  }
})
