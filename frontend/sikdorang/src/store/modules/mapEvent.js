const mapEvent = {
    namespaced : true,
    state : {
        flip : true,
        mouseOver : null,
        mouseOverToCard : null,
        clicked : null,
        threeRes : [],
        selectedRest : null,
        planList : [],
        tags: [],
        tagStores: [],
        selectTag: null,
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
        getmouseOverToCard : state => {
            return state.mouseOverToCard
        },
        getTags : state => {
            return state.tags
        },
        getTagStores : state => {
            return state.tagStores
        },
        getSelectTag : state => {
            return state.selectTag
        }
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
            state.tags = []
            state.tagStores = false
            state.selectTag =null
        },
        mutationMouseOverToCard: (state, payload) => {
            state.mouseOverToCard = payload
        },
        mutationTags: (state, payload) => {
            state.tags = payload
        },
        mutationTagStores: (state, payload) => {
            state.tagStores = payload
        },
        mutationSelectTag: (state, payload) => {
            state.selectTag = payload
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
        actionPlanList: ({commit}, payload) => {
            commit("mutationPlanList", payload)
        },
        actionMapEventClear: ({commit}, payload) => {
            commit("mutationMapEventClear", payload)
        },
        actionMouseOverToCard: ({commit}, payload) => {
            commit("mutationMouseOverToCard", payload)
        },
        actionTags: ({commit}, payload) => {
            commit("mutationTags", payload)
        },
        actionTagStores: ({commit}, payload) => {
            commit("mutationTagStores", payload)
        },
        actionSelectTag: ({commit}, payload) => {
            commit("mutationSelectTag", payload)
        },
    }
}

export default mapEvent