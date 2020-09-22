const schedule = {
    namespaced: true,
    state: {
        schedule: [],
    },
    getters: {
        getSchedules: state => {
            return state.schedule
        },
    },
    mutations: {
        mutationSchedule: (state, payload) => {
            state.schedule = payload
        },
        mutationStore: (state, payload) => {
            state.schedule[payload.index].store = payload.store
        },
    },
    actions: {
        actionSchedule: ({ commit }, payload) => {
            commit("mutationSchedule", payload)
        },
        actionStore: ({ commit }, payload) => {
            commit("mutationStore", payload)
        },
    }
}

export default schedule
