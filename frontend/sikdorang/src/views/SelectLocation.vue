<template>
  <div class="m-5">
        <div class="text-center">
            <v-btn
            color="red lighten-2"
            dark
            @click="getMyLocation"
            >
            내 위치
            </v-btn>

            <v-dialog
            v-model="dialog"
            width="500"
            >
            <template v-slot:activator="{ on, attrs }">
                <v-btn
                color="red lighten-2"
                dark
                v-bind="attrs"
                v-on="on"
                >
                다른 지역
                </v-btn>
            </template>

            <v-card>
                <v-card-title class="headline grey lighten-2">
                지역 검색하기
                </v-card-title>
                <div>
                    <v-card-text>
                    여행을 시작할 지역을 검색해보세요!
                   
                    <template>
                    <v-form>
                        <span>
                        <v-text-field
                            v-model="destination" 
                            @keyup.enter="findPath(destination)"
                            label="어디 갈래?"
                            
                        ></v-text-field>
                        <v-btn
                            color="primary"
                            text
                            @click="findPath(destination)"
                        >
                            검색
                        </v-btn>
                        {{message}}
                        </span>
                    </v-form>
                    <!-- <div id="map"></div> -->
                    </template>
           
                    </v-card-text>
                </div>

                <v-divider></v-divider>

                <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn
                    color="primary"
                    text
                    @click="check"
                >
                    확인
                </v-btn>
                </v-card-actions>
            </v-card>
            </v-dialog>
        </div>
        <div id="map"></div>
  </div>
</template>

<script>
const kakaoMapKey = "d313fa70ad00838acce4a3b5bc134b23";
export default {
    name : 'SelectLocation',
    components : {},
    data() {
        return {
            map : null,
            Latitude: null,
            Longitude: null,
            dialog: false,
            destination: '',
            message : '',
        }
    },
    mounted() {
        if (window.kakao && window.kakao.map) {
			this.initMap();
		}
		else {
			this.addScript();
        }
        
    },
    methods : {
       initMap() { 
			var container = document.getElementById('map'); 
			var options = {
				center: new kakao.maps.LatLng(36.0970073,128.4254652),
				level: 3
			}; 
			var map = new kakao.maps.Map(container, options); 
            this.map = map;
            var marker = new kakao.maps.Marker({position: map.getCenter()}); 
			marker.setMap(map);
			
		},
	
		//cdn 추가
		addScript() { 
			const script1 = document.createElement('script'); 
			/* global kakao */ // 지우면 작동안함
			script1.src = `http://dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=${kakaoMapKey}`;
			document.head.appendChild(script1);

			const script2 = document.createElement('script'); 
			script2.type = "text/javascript";
			script2.src = `//dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=${kakaoMapKey}&libraries=services`;
			document.head.appendChild(script2); 

			script2.onload = () => kakao.maps.load(this.initMap);
		},
        check() {
            this.dialog = false
            this.message = ''
            this.$cookies.set("destination", this.destination)
            this.$cookies.set("searchMethod", "Regions")

            this.destination = ''
            this.$router.push('/map')
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
                    this.$router.push('/map')
                }.bind(this));
                
			} else {
                
                //위치정보 사용 불가능 
				console.log("위치 정보 사용이 불가능합니다.")
			}
        },
        findPath(destination) {
            this.message = ''
            this.destination = destination
            console.log(destination)
            this.message = ` ${destination} 에서 여행을 시작해볼까요? `
            
			var map = this.map

			// 주소-좌표 변환 객체를 생성합니다
			var geocoder = new kakao.maps.services.Geocoder();

			// 주소로 좌표를 검색합니다
			geocoder.addressSearch(this.destination, (result, status) => {

				// 정상적으로 검색이 완료됐으면 
				if (status === kakao.maps.services.Status.OK) {
                    console.log(status)
                    var coords = new kakao.maps.LatLng(result[0].y, result[0].x);
                    console.log(coords)
                    map.setCenter(coords);

				} 
			});       

		

        },
        // findPath(){  
		// 	var map = this.map

		// 	// 주소-좌표 변환 객체를 생성합니다
		// 	var geocoder = new kakao.maps.services.Geocoder();

		// 	// 주소로 좌표를 검색합니다
		// 	geocoder.addressSearch(this.destination, (result, status) => {

		// 		// 정상적으로 검색이 완료됐으면 
		// 		if (status === kakao.maps.services.Status.OK) {
		// 			var coords = new kakao.maps.LatLng(result[0].y, result[0].x);

		// 			// 지도의 중심을 결과값으로 받은 위치로 이동시킵니다
		// 			map.setCenter(coords);
		// 		} 
		// 	});       

		// },

    }

}
</script>

<style>

</style>