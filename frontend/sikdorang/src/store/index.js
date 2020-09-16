import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

import mapEvent from './modules/mapEvent.js'

export default new Vuex.Store({
  state: {
    positions : []
  },
  mutations: {
  },
  actions: {
  },
  modules: {
    mapEvent,
  }
})
