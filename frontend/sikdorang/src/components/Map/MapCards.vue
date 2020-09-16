<template>
  <div>
      <div class="d-flex justify-content-center">
          <div class="box" v-for="rec in threeRec" :key="rec.id">
            {{rec.title}}
            {{rec.latitude}}
            {{rec.longitude}}
            <p>음식점 카테고리</p>
            <p>태그들</p>
          </div>
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
    mounted() {
        this.fillPositions()
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
            this.flip = !this.filp
            if (this.filp) {
                this.threeRec = this.recommendations.slice(0,3)
            }
            else {
                this.threeRec = this.recommendations.slice(3,6)
            }
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