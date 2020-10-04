const party = {
  namespaced: true,
  state: {
    type: 0,
    party: null,
    trip: null,
  },
  getters: {
    getParty: (state) => {
      return state.party
    },
    getTrip: (state) => {
      return state.trip
    },
    getType: (state) => {
      return state.type
    },
  },
  mutations: {
    mutationParty: (state, payload) => {
      state.party = payload
    },
    mutationTrip: (state, payload) => {
      state.trip = payload
    },
    mutationType: (state, payload) => {
      state.type = payload
    },
  },
  actions: {
    actionParty: ({ commit }, payload) => {
      commit("mutationParty", payload)
    },
    actionTrip: ({ commit }, payload) => {
      commit("mutationTrip", payload)
    },
    actionType: ({ commit }, payload) => {
      commit("mutationType", payload)
    },
  },
}

export default party
