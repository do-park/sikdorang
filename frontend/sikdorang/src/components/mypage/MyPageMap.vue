<template>
    <div class="map-wrap">
        <div id="map"></div>
        <p>{{ plans }}</p>
    </div>
</template>

<script>
import { mapGetters } from "vuex"

const kakaoMapKey = "d313fa70ad00838acce4a3b5bc134b23";
const mypage = "mypage"

export default {
    name: "MyPageMap",
    data() {
        return {
            plans : [],
        }
    },
    methods: {
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
			
			this.startCoord();
			this.initCurLocation();
        },
        initCurLocation() {
			this.curLat = this.startLat
			this.curLong = this.startLong
        },
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
        startCoord() {
			var map = this.map
			
            if (this.$cookies.get("searchMethod")==="myLocation"){
            this.startLat = this.$cookies.get("startLatitude")
            this.startLong = this.$cookies.get("startLongitude")

            var LatLng = new kakao.maps.LatLng(this.startLat, this.startLong)
            map.setCenter(LatLng);
			var marker = new kakao.maps.Marker({ position: map.getCenter() });
			marker.setMap(map);

            }
            else {
                this.destination = this.$cookies.get('destination')

                // 주소-좌표 변환 객체를 생성합니다
                var geocoder = new kakao.maps.services.Geocoder();

                // 주소로 좌표를 검색합니다
                geocoder.addressSearch(this.destination, (result, status) => {

                    // 정상적으로 검색이 완료됐으면 
                    if (status === kakao.maps.services.Status.OK) {
                        var coords = new kakao.maps.LatLng(result[0].y, result[0].x);

                        // 지도의 중심을 결과값으로 받은 위치로 이동시킵니다
						map.setCenter(coords);
						console.log(`${this.destination} 좌표 : ${coords} `)
                        var marker = new kakao.maps.Marker({ position: map.getCenter() });
                        marker.setMap(map);
                    } 
                })
            }
        },
		showPaths() {
			var plans = this.plans;
			var map = this.map;
			var positions = plans;
			var imageSrc = "https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/markerStar.png"; 
			var bounds = new kakao.maps.LatLngBounds();   
						
			for (var i = 1; i < positions.length; i ++) {
					
				var linePath = [
					positions[i-1].latlng,
					positions[i].latlng 
				];

				// 지도에 표시할 선을 생성합니다
				var polyline = new kakao.maps.Polyline({
					path: linePath, // 선을 구성하는 좌표배열 입니다
					strokeWeight: 5, // 선의 두께 입니다
					strokeColor: '#FFAE00', // 선의 색깔입니다
					strokeOpacity: 0.7, // 선의 불투명도 입니다 1에서 0 사이의 값이며 0에 가까울수록 투명합니다
					strokeStyle: 'solid' // 선의 스타일입니다
				});

				// 지도에 선을 표시합니다 
				polyline.setMap(map); 
				var distance = Math.round(polyline.getLength());
				var content = this.getTimeHTML(distance);

				// 커스텀 오버레이를 생성하고 지도에 표시합니다
				var distanceOverlay = new kakao.maps.CustomOverlay({
					map: map, // 커스텀오버레이를 표시할 지도입니다
					content: content,  // 커스텀오버레이에 표시할 내용입니다
					position: positions[i].latlng, // 커스텀오버레이를 표시할 위치입니다.
					xAnchor: 0,
					yAnchor: 0,
					zIndex: 3  
				}); 

				distanceOverlay.setMap(map)
			}

			plans.forEach(plan=>{

				// 마커 이미지의 이미지 크기 입니다
				var imageSize = new kakao.maps.Size(24, 35); 
				
				// 마커 이미지를 생성합니다    
				var markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize); 
				
				// 마커를 생성합니다
				var marker = new kakao.maps.Marker({
					map: map,
					position: plan.latlng,
					title : plan.title,
					image : markerImage
				});

				bounds.extend(plan.latlng);
				marker.setMap(map);
			})
							
			// LatLngBounds 객체에 추가된 좌표들을 기준으로 지도의 범위를 재설정합니다
			// 이때 지도의 중심좌표와 레벨이 변경될 수 있습니다
			map.setBounds(bounds);			
		},
    },
    computed: {
        ...mapGetters(mypage, [
            "getClickedTrip"
        ])
    },
    watch: {
        getClickedTrip(val) {
            val.forEach(el => {
                el.latlng = new kakao.maps.LatLng(el.lat, el.lng)
            })
            console.log(val)
            this.plans = val
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
    
}
</script>

<style>

</style>