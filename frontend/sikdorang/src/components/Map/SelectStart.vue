<template>
  <div>
    <div class="text-center">
        <button type="button" class="btn btn-secondary" @click="getMyLocation">내 위치</button>
        <!-- Button trigger modal -->
        <button type="button" class="btn btn-secondary" data-toggle="modal" data-target="#exampleModal">
        다른 지역
        </button>

        <!-- Modal -->
        <div class="modal fade" id="exampleModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="exampleModalLabel">지역 검색하기</h5>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                <span aria-hidden="true">&times;</span>
                </button>
            </div>
            <div class="modal-body">
                여행을 시작할 지역을 검색해보세요!
                <br>
                    <input
                        v-model="destination" 
                        @keyup.enter="findPath(destination)"
                        label="어디 갈래?"
                        placeholder="예시) XX동 or XX동 775-5"
                    />
                    <button class="btn btn-secondary" @click="findPath(destination)">
                        검색
                    </button>
                    <br>
                    {{message}}
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-dismiss="modal">닫기</button>
                <button type="button" class="btn btn-primary" @click="check">확인</button>
            </div>
            </div>
        </div>
        </div>

    </div>
  </div>
</template>

<script>
export default {
    name : 'SelectStart',
    data() {
        return {
            Latitude: null,
            Longitude: null,
            dialog: false,
            destination: '',
            message : '',
        }
    },
 
    methods : {
        check() {
            this.dialog = false
            this.message = ''
            this.$cookies.set("searchMethod", "Regions")
            this.destination = ''
            this.$emit("flag",false)
           
        },
        getMyLocation() {	
			if('geolocation' in navigator) {
                
                //위치 요청
				navigator.geolocation.getCurrentPosition(function(pos) {
					this.Latitude = pos.coords.latitude;
					this.Longitude = pos.coords.longitude;
                    alert("현재 위치는 : " + this.Latitude + ", "+ this.Longitude);
                    
                    //시작 위도,경도 쿠키에 올리기
                    console.log(this.Latitude,this.Longitude)
                    this.$cookies.set('startLatitude',this.Latitude)
                    this.$cookies.set('startLongitude',this.Longitude)
                    this.$cookies.set("searchMethod", "myLocation")
                    this.$emit("flag",false)
                    
                }.bind(this));
                
			} else {
                
                //위치정보 사용 불가능 
				console.log("위치 정보 사용이 불가능합니다.")
			}
        },
        
        findPath(destination) {
            this.destination = destination
            this.message = `${destination}에서 시작해볼까요?`
            this.$cookies.set("destination", destination)
        },
      
    }

}
</script>

<style>

</style>