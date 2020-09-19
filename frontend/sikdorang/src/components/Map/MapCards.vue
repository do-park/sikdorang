<template>
  <div>
      <div>flip : {{ getFlip }}</div>

        <!-- Modal -->
        <div class="modal fade" id="exampleModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="exampleModalLabel">
                    <div v-if="getSelectedRest">{{getSelectedRest.title}}</div>
                    <div v-else>어떤 식당을 찾으시나요?</div>
                </h5>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                <span aria-hidden="true">&times;</span>
                </button>
            </div>
            <div class="modal-body">
                
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-dismiss="modal">닫기</button>
                <button type="button" class="btn btn-primary">일정 저장하기</button>
            </div>
            </div>
        </div>
        </div>
            
      <div class="d-flex flex-column align-items-center">
      <div>
          <button class="btn btn-secondary" @click="checkFilp">다른거 볼래요</button>
      </div>
      <div class="d-flex justify-content-center">
          <div 
            :class="{ 'active': isActive0 }"
            class="box" 
            @click="selectRest(getThreeRes[0])"
            data-toggle="modal" 
            data-target="#exampleModal"
          >
            A.{{getThreeRes[0].title}}
            <p>@ 맛집 정보 @</p>
          </div>
          <div 
            :class="{ 'active': isActive1 }"
            class="box" 
            @click="selectRest(getThreeRes[1])"
            data-toggle="modal" 
            data-target="#exampleModal"
          >
            B.{{getThreeRes[1].title}}
            <p>@ 맛집 정보 @</p>
          </div>
          <div 
            :class="{ 'active': isActive2 }"
            class="box" 
            @click="selectRest(getThreeRes[2])"
            data-toggle="modal" 
            data-target="#exampleModal"
          >
            C.{{getThreeRes[2].title}}
            <p>@ 맛집 정보 @</p>
          </div>
        
          <br> 
        </div>
      </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex"
const mapEvent = "mapEvent"

export default {
    name : 'MapCards',
    data() {
        return {
            
            recommendations : [],
            isActive0 : false,
            isActive1 : false,
            isActive2 : false,
        }
    },
    props : {
        kakao : Object,
    },
    computed : {
        ...mapGetters(mapEvent, [
            'getFlip',
            'getMouseOver',
            'getClicked',
            'getThreeRes',
            'getSelectedRest'   
        ])
    },
    watch : {
        getMouseOver() {
            this.changeOverBox(this.getMouseOver)
        },
        getClicked() {
            this.actionSelectedRest(this.getThreeRes[this.getClicked])
        },
        getThreeRes() {
            console.log(this.getThreeRes)
            this.actionSelectedRest = this.getThreeRes[0];
        }
        
    },
    mounted() {
        this.fillPositions()
        this.checkFilp()
        
    },
    methods : {
        ...mapActions(mapEvent, [
            'actionFlip',
            'actionSelectedRest'


        ]),
        selectRest(rest) {
            this.actionSelectedRest(rest)
        },
        changeOverBox(overidx){ 
           
            this.isActive0 = false
            this.isActive1 = false
            this.isActive2 = false
           

           if (overidx === 0) {
               this.isActive0 = true
           }
           else if (overidx === 1) {
               this.isActive1 = true
           }
           else if (overidx === 2) {
               this.isActive2 = true
           }
           else{
             
            this.isActive0 = false
            this.isActive1 = false
            this.isActive2 = false
           
           }

            
        },
        fillPositions() {
			this.recommendations = [
				{   
					id : 1,
					title: '승희 위치', 
                    latitude: 36.1406514,
                    longitude : 128.3271104
				},
				{   
					id : 2,
                    title: '인영이집', 
                    latitude: 36.1035992,
                    longitude : 128.4162945
				},
				{   
					id : 3,
                    title: '규성집', 
                    latitude: 36.0954328,
                    longitude : 128.3963511
				},
				{   
					id : 4,
                    title: '성수집근처쨈나',
                    latitude: 36.1115959,
                    longitude : 128.4303873

				},
				{   
					id : 5,
                    title: '도희동아백화점',
                    latitude: 36.119735,
                    longitude : 128.3463003
				},
				{   
					id : 6,
                    title: '인동스타벅스',
                    latitude: 36.1073795,
                    longitude : 128.4174558
				}
            ]
        },
        checkFilp() {
            console.log("MapCards getFlip",this.getFlip)
            this.actionFlip(!this.getFlip)
        },
    }
}
</script>

<style>
.box{
    margin: 2px;
    text-align: center;
    background-color : lightgray;
    width : 130px;
}
.box:hover{
    cursor: pointer;
    background-color: lightblue;
}
.active{
    cursor: pointer;
    background-color: lightblue;
}

</style>