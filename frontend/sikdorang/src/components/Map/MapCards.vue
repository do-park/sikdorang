<template>
  <div>
      <div>{{flip}}</div>
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
            <p>음식점 카테고리</p>
            <p>태그들</p>
          </div>
          <button @click="checkFilp">다른거 볼래요</button>

      </div>
  </div>
</template>

<script>
export default {
    name : 'MapCards',
    data() {
        return {
            threeRec : [],
            recommendations : [],
            filp : false,
        }
    },
    props : {
        selected : Number,
    },
    mounted() {
        this.fillPositions()
        console.log("MapCard mounted",this.flip)
    },
    methods : {
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
            console.log(this.recommendations)
            this.threeRec = this.recommendations.slice(0,3)
            console.log(this.threeRec)
        },
        checkFilp() {
            if (this.flip === null ) {
                this.flip = this.$cookies.get('flip')
            }
            console.log("before",this.flip,!!this.flip)
            if (this.filp === true ) {
                console.log("true->false")
                this.flip = false
                this.threeRec = this.recommendations.slice(3,6)
            }
            else {
                console.log("false->true")
                this.flip = true
                this.threeRec = this.recommendations.slice(0,3)
            }
            console.log("after",this.flip)
            this.$cookies.set('flip',this.flip)
        },
    },
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