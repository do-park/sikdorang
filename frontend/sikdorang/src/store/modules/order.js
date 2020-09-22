const order = {
    namespaced: true,
    state: {
        orderTrip: null,
    },
    getters: {
        getOrderTrip: state => {
            return state.orderTrip
        },
    },
    mutations: {
        mutationOrderTrip: (state, payload) => {
            state.orderTrip = payload
        },
    },
    actions: {
        actionOrderTrip: ({ commit }, payload) => {
            commit("mutationOrderTrip", payload)
        },
    }
}

export default order