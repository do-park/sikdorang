<template>
  <div>
  </div>
</template>

<script>
import swal from 'sweetalert';
import { mapActions, mapGetters } from "vuex"
// import jQuery from 'jquery';
// let $ = jQuery;
const mapEvent = "mapEvent"
export default {
    name : 'MarkerModal',
    computed : {
        ...mapGetters(mapEvent, [
            'getClicked',
            'getThreeRes',
            'getSelectedRest'
        ])
    },
    watch : {
        getClicked() {
            this.selectRest(this.getClicked)
        },
    },
    methods : {
        ...mapActions(mapEvent,[
            'actionClicked',
            'actionSelectedRest',
        ]),
        selectRest(idx) {
            this.actionClicked(idx)
            this.actionSelectedRest(this.getThreeRes[idx])
            var Rest = this.getSelectedRest
            swal({
            title: Rest.title,
            text: "이런이런 맛집입니다아",
            buttons: ["취소","추가"],
            })
            .then((res) => {
            if (res) {
                swal(`${Rest.title}을 일정에 추가할까요?`,{
                    buttons: ["아니오","네"],
                })
                .then((res)=>{
                    if (res) {
                        swal(`${Rest.title}을 일정에 추가할까요?`,{
                        icon : "success"
                        })
                        
                    }
                })
            } 
        });

        
        },

    }

}
</script>

<style>
.modal-active{
	display:block;
}
</style>