const mypage = {
    namespaced: true,
    state: {
        userInfo: {
            userName: null,
            userBirth: null,
            userPhone: null,
        },
        tripList: [],
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
            if (state.tripList !== null) {
                return state.tripList[state.clickedIndex]
            } else {
                return { id: 0, title: "시작점", lan: 36.0970073, lng: 128.4254652 }
            }
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
            commit("mutationUserInfo", payload)
        },
        actionTripList: ({ commit }, payload) => {
            commit("mutationTripList", payload)
        },
        actionClickedIndex: ({ commit }, payload) => {
            commit("mutationClickedIndex", payload)
        }
    }
}

export default mypage