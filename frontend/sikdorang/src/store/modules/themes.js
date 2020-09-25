const themes = {
  namespaced: true,
  state: {
    themes: [
      { id: 1, db_id: 5, theme_name: "빵집" },
      { id: 2, db_id: 6, theme_name: "케익" },
      { id: 3, db_id: 1, theme_name: "만두" },
      { id: 4, db_id: 3, theme_name: "떡볶이" },
      { id: 5, db_id: 7, theme_name: "짬뽕" },
      { id: 6, db_id: 2, theme_name: "짜장면" },
      { id: 7, db_id: 8, theme_name: "수제버거" },
      { id: 8, db_id: 10, theme_name: "돈가스" },
      { id: 9, db_id: 11, theme_name: "터미널" },
      { id: 10, db_id: 4, theme_name: "기차역" },
      { id: 11, db_id: 9, theme_name: "휴게소" },
    ],
    themeClear: [0] * 12,
    storeClear: [0] * 150,
  },
  getters: {
    getThemes: (state) => {
      return state.themes
    },
    getThemesClear: (state) => {
      return state.themeClear
    },
    getStoreClear: (state) => {
      return state.storeClear
    },
  },
  mutations: {
    mutationThemes: (state, payload) => {
      state.themes = payload
    },
    mutationThemesClear: (state, payload) => {
      state.themeClear = payload
    },
    mutationStoreClear: (state, payload) => {
      state.storeClear = payload
    },
  },
  actions: {
    actionThemes: ({ commit }, payload) => {
      commit("mutationThemes", payload)
    },
    actionThemesClear: ({ commit }, payload) => {
      commit("mutationThemesClear", payload)
    },
    actionStoreClear: ({ commit }, payload) => {
      commit("mutationStoreClear", payload)
    },
  },
}

export default themes
