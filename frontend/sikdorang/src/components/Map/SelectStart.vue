<template>
  <div>
    <div class="text-center">
        <button type="button" class="btn btn-secondary" @click="getMyLocation">내 위치</button>
        <!-- <button class="btn btn-secondary" @click="search">다른 지역</button> -->

    </div>
  </div>
</template>

<script>
import swal from 'sweetalert';
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
        // search() {
        //     swal({
        //     title: "어느 지역을 검색하시겠습니까?",
        //     content: "input",
        //     buttons: true,
        //     })
        //     .then((value) => {
        //     if (value) {
        //         swal(`${value}에서 시작해볼까요?`,{
        //             buttons: true,
        //         })
        //         .then((res)=>{
        //             if (res) {
        //                 console.log(res,"ok눌렀다")
        //                 this.$cookies.set("searchMethod", "Regions")
        //                 this.$cookies.set("destination", value)
        //                 this.destination = ''
        //                 this.$emit("flag",false)
        //             }
        //         })
                
        //     } else {
        //         swal("검색어를 입력해주세요.", {
        //         icon: "warning",
        //         dangerMode: true,
        //         } ) 
        //     }
        //     });

        // },
      
        getMyLocation() {	
			if('geolocation' in navigator) {
                
                //위치 요청
				navigator.geolocation.getCurrentPosition(function(pos) {
					this.Latitude = pos.coords.latitude;
                    this.Longitude = pos.coords.longitude;
                    swal("내 위치", this.Latitude + ", "+ this.Longitude, "success")
                    .then((res)=>{
                        if (res) {
                            //시작 위도,경도 쿠키에 올리기
                            this.$cookies.set('startLatitude',this.Latitude)
                            this.$cookies.set('startLongitude',this.Longitude)
                            this.$cookies.set("searchMethod", "myLocation")
                            this.$emit("flag",false)
                        }
                    })
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