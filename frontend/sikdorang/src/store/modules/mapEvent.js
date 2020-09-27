const mapEvent = {
    namespaced : true,
    state : {
        flip : true,
        mouseOver : null,
        clicked : null,
        threeRes : [],
        selectedRest : null,
        planList : [],
    },
    getters : {
        getFlip : state => {
            return state.flip
        },
        getMouseOver : state => {
            return state.mouseOver
        },
        getClicked : state => {
            return state.clicked
        },
        getThreeRes : state => {
            if (state.threeRes) {
                return state.threeRes
            }
        },
        getSelectedRest : state => {
            return state.selectedRest
        },
        getPlanList : state => {
            return state.planList
        },
    },
    mutations : {
        mutationFlip: (state,payload) => {
            state.flip = payload
        },
        mutationMouseOver: (state,payload) => {
            state.mouseOver = payload
        },
        mutationClicked: (state,payload) => {
            state.clicked = payload
        },
        mutationThreeRes: (state,payload) => {
            state.threeRes = payload
        },
        mutationSelectedRest: (state,payload) => {
            state.selectedRest = payload
        },
        mutationPlanList: (state,payload) => {
            state.planList = payload
        },
        mutationMapEventClear: (state) => {
            state.flip = true
            state.mouseOver = null
            state.clicked = null
            state.threeRes = []
            state.selectedRest = null
            state.planList = []
        }
    },
    actions : {
        actionFlip: ({commit}, payload) => {
            commit("mutationFlip", payload)
        },
        actionMouseOver: ({commit}, payload) => {
            commit("mutationMouseOver", payload)
        },
        actionClicked: ({commit}, payload) => {
            commit("mutationClicked", payload)
        },
        actionThreeRes: ({commit}, payload) => {
            commit("mutationThreeRes", payload)
        },
        actionSelectedRest: ({commit}, payload) => {
            commit("mutationSelectedRest", payload)
        },
        actionPlanList: ({commit}, payload) => {
            commit("mutationPlanList", payload)
        },
        actionMapEventClear: ({commit}, payload) => {
            commit("mutationMapEventClear", payload)
        },
    }
}

export default mapEvent