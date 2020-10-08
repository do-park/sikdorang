const schedule = {
  namespaced: true,
  state: {
    schedule: [],
    scheduleIdx: 0,
    scheduleProgressIdx: -1,
    scheduleName: "",
    scheduleDate: 0,
    beforeCat: [],
  },
  getters: {
    getSchedules: (state) => {
      return state.schedule
    },
    getScheduleIdx: (state) => {
      return state.scheduleIdx
    },
    getScheduleProgressIdx: (state) => {
      return state.scheduleProgressIdx
    },
    getScheduleName: (state) => {
      return state.scheduleName
    },
    getScheduleDate: (state) => {
      return state.scheduleDate
    },
    getBeforeCat: (state) => {
      return state.beforeCat
    },
  },
  mutations: {
    mutationSchedule: (state, payload) => {
      state.schedule = payload
    },
    mutationStore: (state, payload) => {
      // state.schedule[payload.index].userChoice = payload
      state.schedule[state.scheduleIdx].userChoice = payload
      state.beforeCat.push(payload.category)
    },
    mutationScheduleIdx: (state, payload) => {
      state.scheduleIdx = payload
    },
    mutationScheduleProgressIdx: (state, payload) => {
      state.scheduleProgressIdx = payload
    },
    mutationScheduleName: (state, payload) => {
      state.scheduleName = payload
    },
    mutationScheduleDate: (state, payload) => {
      state.scheduleDate = payload
    },
    mutationClearBeforeCat: (state) => {
      state.beforeCat = []
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
    actionscheduleProgressIdx: ({ commit }, payload) => {
      commit("mutationScheduleProgressIdx", payload)
    },
    actionScheduleName: ({ commit }, payload) => {
      commit("mutationScheduleName", payload)
    },
    actionScheduleDate: ({ commit }, payload) => {
      commit("mutationScheduleDate", payload)
    },
    actionClearBeforeCat: ({ commit }) => {
      commit("mutationClearBeforeCat")
    },
  },
}

export default schedule
