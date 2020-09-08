<template>
  <div>
		<button @click="addPositions">보여주나?</button>
		<br>
		<div class="map-top">
			<div class="search-tap">
					
				<!-- 길찾기  -->
				<span> 
					<input
					id="search-box"
					v-model="destination" 
					@keyup.enter="findPath()"
					placeholder="어디갈래?">
					<button id="search-btn" @click="findPath()" >아이콘</button>
				</span>
			</div>
			
			<div class="tag-tap">
				<button>#위대한</button>
				<button>#가성비</button>
				<button>#갬성</button>
				<button>#어쩌구</button>
				<!-- <button>#저쩌구</button>
				<button>#스크롤을</button>
				<button>#시도해보자</button> -->
			</div>
		</div>
		<div class="map-wrap">
			<div id="map"></div>
		</div>
		<div>
				<div>보여주는곳</div>
				<div id="show-place"></div>
		</div>
     
  </div>
</template>

<script>
const kakaoMapKey = 'd313fa70ad00838acce4a3b5bc134b23';
export default {
    name : 'MapTest',
    data() {
        return {
            destination : '',
            map: null,
        }
    },
    mounted() {
        if (window.kakao && window.kakao.map) {
            this.initMap()
        }
        else {
            this.addScript()
        }
        // window.kakao && window.kakao.maps ? this.initMap() : this.addScript();
        // this.addPositions()
    },
    methods : {
        //맵 생성
        initMap() { 
            var container = document.getElementById('map'); 
            var options = {
                center: new kakao.maps.LatLng(36.0970073,128.4254652),
                level: 3
            }; 
            var map = new kakao.maps.Map(container, options); 
            this.map = map
            //마커추가하려면 객체를 아래와 같이 하나 만든다. 
            var marker = new kakao.maps.Marker({position: map.getCenter()}); 
            marker.setMap(map);
           
        }, 
        
        //cdn 추가
        addScript() { 
            const script1 = document.createElement('script'); 
            /* global kakao */ 
            script1.src = `http://dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=${kakaoMapKey}`;
            document.head.appendChild(script1);

            const script2 = document.createElement('script'); 
            script2.type = "text/javascript"
            script2.src = `//dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=${kakaoMapKey}&libraries=services`;
            document.head.appendChild(script2); 

            script2.onload = () => kakao.maps.load(this.initMap);
        },

        //여러개 위치 보여주는 함수
        addPositions() {
            var mapContainer = document.getElementById('map'), // 지도를 표시할 div  
            mapOption = { 
                center: new kakao.maps.LatLng(36.0970073,128.4254652), // 지도의 중심좌표
                level: 3 // 지도의 확대 레벨
            };

            var map = new kakao.maps.Map(mapContainer, mapOption);
            var positions = [
                {
                    title: '승희 위치', 
                    latlng: new kakao.maps.LatLng(36.0970073,128.4254652)
                },
                {
                    title: '인영이집', 
                    latlng: new kakao.maps.LatLng(36.1035992,128.4162945)
                },
                {
                    title: '규성집', 
                    latlng: new kakao.maps.LatLng(36.0954328,128.3963511)
                },
                {
                    title: '성수집근처쨈나',
                    latlng: new kakao.maps.LatLng(36.1115959,128.4303873)

                },
                {
                    title: '도희동아백화점',
                    latlng: new kakao.maps.LatLng(36.119735,128.3463003)
                }
            ];
            var imageSrc = "https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/markerStar.png"; 
                
            for (var i = 0; i < positions.length; i ++) {
                
                // 마커 이미지의 이미지 크기 입니다
                var imageSize = new kakao.maps.Size(24, 35); 
                
                // 마커 이미지를 생성합니다    
                var markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize); 
                
                // 마커를 생성합니다
                var marker = new kakao.maps.Marker({
                    map: map, // 마커를 표시할 지도
                    position: positions[i].latlng, // 마커를 표시할 위치
                    title : positions[i].title, // 마커의 타이틀, 마커에 마우스를 올리면 타이틀이 표시됩니다
                    image : markerImage // 마커 이미지 
                });
                marker.setMap(map);


                kakao.maps.event.addListener(marker, 'click', makeOverListener(map, marker));
            }

            function makeOverListener(map, marker) {
                return function() {
                    document.getElementById("show-place").innerHTML = marker.mc
                    console.log(marker) 
                };
            }
        },
        
        findPath(){  
					var map = this.map
					// 주소-좌표 변환 객체를 생성합니다
					var geocoder = new kakao.maps.services.Geocoder();

					// 주소로 좌표를 검색합니다
					geocoder.addressSearch(this.destination, (result, status) => {

							// 정상적으로 검색이 완료됐으면 
							if (status === kakao.maps.services.Status.OK) {

									var coords = new kakao.maps.LatLng(result[0].y, result[0].x);

									// 지도의 중심을 결과값으로 받은 위치로 이동시킵니다
									map.setCenter(coords);
							} 
					});       

        }
    }, 

}


</script>

<style>

.map-top {
	position: absolute;
	z-index: 10;
	width: 100%;
	margin: auto;
	
}

.search-tap {
	background-color: rgba(255, 255, 255, 0.8);
	width: 400px;
	margin: auto;
}

#search-box {
    width: 342px;
    height: 30px;
    float: left;
}

#search-btn {
    width: 50px;
    height: 36px;
    float: right;
}

.tag-tap {
	width: 400px;
	margin: auto;
}

.tag-tap > button {
	margin: 10px;
	background-color: yellow;
}

#map {
	width: 400px;
	height: 500px;
	margin-left: auto;
	margin-right: auto;
}

</style>