const mapEvent = {
    namespaced : true,
    state : {
        flip : false,
        mouseOver : null,
        clicked : null,
        threeRes : null,
        selectedRest : null,
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
            return state.threeRes
        },
        getSelectedRest : state => {
            return state.selectedRest
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
    }
}

export default mapEvent