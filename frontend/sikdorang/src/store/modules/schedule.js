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
        mutationLatlng: (state, payload) => {
            state.schedule[payload.index].latlng = payload.latlng
        }
    },
    actions: {
        actionSchedule: ({ commit }, payload) => {
            commit("mutationSchedule", payload)
        },
        actionStore: ({ commit }, payload) => {
            commit("mutationStore", payload)
        },
        actionLatlng: ({ commit }, payload) => {
            commit("mutationLatlng", payload)
        }
    }
}

export default schedule
