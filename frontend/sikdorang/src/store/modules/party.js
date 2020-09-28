const party = {
  namespaced: true,
  state: {
    party: [],
  },
  getters: {
    getParty: (state) => {
      return state.party
    },
  },
  mutations: {
    mutationParty: (state, payload) => {
      state.party = payload
    },
  },
  actions: {
    actionParty: ({ commit }, payload) => {
      commit("mutationParty", payload)
    },
  },
}

export default party
