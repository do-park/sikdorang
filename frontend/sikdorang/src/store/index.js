import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

import mypage from './modules/mypage.js'

export default new Vuex.Store({
  state: {
  },
  mutations: {
  },
  actions: {
  },
  modules: {
    mypage: mypage,
  }
})
