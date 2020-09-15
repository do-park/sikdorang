const mypage = {
    namespaced: true,
    state: {
        userInfo: null,
        tripList: null,
        clickedIndex: null,
    },
    getters: {
        getUserInfo: state => {
            return state.userInfo
        },
        getTripList: state => {
            return state.tripList
        },
        getClickedTrip: state => {
            return state.tripList[state.clickedIndex]
        },
    },
    mutations: {
        mutationUserInfo: (state, payload) => {
            state.userInfo = payload
        },
        mutationTripList: (state, payload) => {
            state.tripList = payload
        },
        mutationClickedIndex: (state, payload) => {
            state.clickedIndex = payload
        }
    },
    actions: {
        actionUserInfo: ({ commit }, payload) => {
            commit('mutationUserInfo', payload)
        },
        actionTripList: ({ commit }, payload) => {
            commit('mutationTripList', payload)
        },
        actionClickedIndex: ({ commit }, payload) => {
            commit('mutationClickedIndex', payload)
        }
    }
}

export default mypage