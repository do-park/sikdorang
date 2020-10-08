const sikRec = {
    namespaced: true,
    state: {
        forUser: null,
        isSik: false,
    },
    getters: {
        getForUser: state => {
            return state.forUser
        },
        getIsSik: state => {
            return state.isSik
        },
    },
    mutations: {
        mutationForUser: (state, payload) => {
            state.forUser = payload
        },
        mutationIsSik: (state, payload) => {
            state.isSik = payload
        },
    },
    actions: {
        actionForUser: ({ commit }, payload) => {
            commit("mutationForUser", payload)
        },
        actionIsSik: ({ commit }, payload) => {
            commit("mutationIsSik", payload)
        },
    }
}

export default sikRec