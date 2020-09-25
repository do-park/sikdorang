const schedule = {
    namespaced: true,
    state: {
        schedule: [],
        scheduleIdx : 0,
    },
    getters: {
        getSchedules: state => {
            return state.schedule
        },
        getScheduleIdx: state => {
            return state.scheduleIdx
        },
    },
    mutations: {
        mutationSchedule: (state, payload) => {
            state.schedule = payload
        },
        mutationStore: (state, payload) => {
            // state.schedule[payload.index].userChoice = payload
            state.schedule[state.scheduleIdx].userChoice = payload
        },
        mutationScheduleIdx: (state, payload) => {
            state.scheduleIdx = payload
        },
    },
    actions: {
        actionSchedule: ({ commit }, payload) => {
            commit("mutationSchedule", payload)
        },
        actionStore: ({ commit }, payload) => {
            commit("mutationStore", payload)
        },
        actionScheduleIdx: ({ commit }, payload) => {
            commit("mutationScheduleIdx", payload)
        },
    }
}

export default schedule
