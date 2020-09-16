<template>
  <div>
      <div>flip : {{ getFlip }}</div>
      <div v-if="getClicked">{{threeRec[getClicked].title}}디테일 보여주기</div>
      <div class="d-flex justify-content-center">
          <div 
          class="box" 
          v-for="rec in threeRec" 
          :key="rec.id"
          @click="selectRest()"
          >
            {{rec.title}}
            {{rec.latitude}}
            {{rec.longitude}}
          </div>
          <button @click="checkFilp">다른거 볼래요</button>

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
            threeRec : [],
            recommendations : [],
            selected : null,
        }
    },
    props : {
        kakao : Object,
    },
    computed : {
        ...mapGetters(mapEvent, [
            'getFlip',
            'getMouseOver',
            'getClicked'
            
        ])
    },
    watch : {
        getMouseOver() {
            console.log(this.getMouseOver,"자세히 볼까요?")

        },
        getClicked() {
            console.log(this.getClicked,"디테일 모달입니다.")
            this.moveToClicked()
        },
    },
    mounted() {
        this.fillPositions()
        this.checkFilp()
        this.selected = this.$cookies.get('selectedMarker')
        
    },
    methods : {
        ...mapActions(mapEvent, [
            'actionFlip',

        ]),

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
            console.log("before",this.getFlip,!this.getFlip)
            if (this.getFlip) {
                this.threeRec = this.recommendations.slice(3,6)
               
                
            }
            else {
                this.threeRec = this.recommendations.slice(0,3)
                
                
            }
            this.actionFlip(!this.getFlip)
            console.log("after",this.getFlip)
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

</style>