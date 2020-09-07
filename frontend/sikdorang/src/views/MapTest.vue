<template>
  <div>
		<div class="map-top">
			<div class="search-tap">
				<button @click="addPositions">보여주나?</button>
				<br>
					
				<!-- 길찾기  -->
				<span>To : 
					<input 
					v-model="destination" 
					@keyup.enter="findPath(destination)"
					placeholder="어디갈래?">
					<button @click="findPath(destination)" >길찾기 가보자</button>
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
            //마커추가하려면 객체를 아래와 같이 하나 만든다. 
            var marker = new kakao.maps.Marker({position: map.getCenter()}); 
            marker.setMap(map);
           
        }, 
        
        //cdn 추가
        addScript() { 
            const script = document.createElement('script'); 
            /* global kakao */ 
            script.onload = () => kakao.maps.load(this.initMap); 
            script.src = `http://dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=${kakaoMapKey}`;
            document.head.appendChild(script); 
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
        
        findPath(destination){
            this.destination = destination
            console.log(this.destination)

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