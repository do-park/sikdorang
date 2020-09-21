const theme = {
    namespaced : true,
    state : {
        themes : 
        [
            {"id":1, "theme":"빵집"},
            {"id":2, "theme":"케익"},
            {"id":3, "theme":"만두"},
            {"id":4, "theme":"떡볶이"},
            {"id":5, "theme":"짬뽕"},
            {"id":6, "theme":"짜장면"},
            {"id":7, "theme":"빵집"},
            {"id":8, "theme":"케익"},
            {"id":9, "theme":"수제버거"},
            {"id":10, "theme":"기차역 맛집"},
            {"id":11, "theme":"고속도로 휴게소 맛집"},
            {"id":12, "theme":"전국 터미널 맛집"},
            ]
    },
    getters : {
        getThemes : state => {
            return state.themes
        },
      
    },
    mutations : {
        mutationThemes: (state,payload) => {
            state.themes = payload
        },
       
    },
    actions : {
        actionThemes: ({commit}, payload) => {
            commit("mutationThemes", payload)
        },
        
    }
}

export default theme










