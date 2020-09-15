<template>
  <div>
      {{destination}}
    <!-- <button @click="showPositions(positions)">보여주나?</button> -->
		<br>
    <!-- <button @click="showPaths()">일정 보기 </button> -->
		
		<div class="map-wrap">
			<div id="map"></div>
		</div>
		<div>
			<div>보여주는곳</div>
			<div id="show-place"></div>
		</div>

		<h3>일정 추가해보세요</h3>
		<span 
		v-for="temp in temps" 
		:key="temp.id"
		>
			<button @click="makePlan(temp)">{{temp.title}}</button>
		</span>
		<!-- <h3>일정<button @click="resetPlans()">RESET</button></h3> -->
		<span 
		v-for="plan in plans" 
		:key="plan.id"
		>
			<!-- <button @click="showNewMap(plan.latlng)">{{plan.title}}</button> -->
		</span>   
  </div>
</template>

<script>
import axios from 'axios'
const kakaoMapKey = "d313fa70ad00838acce4a3b5bc134b23";
export default {
	name : "MapField",
	data() {
		return {
			destination : '',
			map: null,
			startLat :36.109328,
			startLong :128.4128223,
			curLat: null,
			curLong: null,
			plans : [],
			temps : [],
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
			
			this.startCoord();
			this.fillPositions();
			this.initCurLocation();
		},

		initCurLocation() {
			this.curLat = this.startLat
			this.curLong = this.startLong
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
		
		getList() {
			//axios로 현재 좌표를 보내면 추천 음식점 6개 받아온다.
			axios.get('/getRests', Headers)
			.then(res => {

			})
			.catch(res=>{

			})
			//선택 음식점 주변의 관광지/카페 정보를 얻는다.
			axios.get('/getRests', Headers)
			.then(res => {

			})
			.catch(res=>{
				
			})
		},

		fillPositions() {
			this.temps = [
				{   
					id : 1,
					title: '승희 위치', 
					latlng: new kakao.maps.LatLng(36.1406514,128.3271104)
				},
				{   
					id : 2,
					title: '인영이집', 
					latlng: new kakao.maps.LatLng(36.1035992,128.4162945)
				},
				{   
					id : 3,
					title: '규성집', 
					latlng: new kakao.maps.LatLng(36.0954328,128.3963511)
				},
				{   
					id : 4,
					title: '성수집근처쨈나',
					latlng: new kakao.maps.LatLng(36.1115959,128.4303873)

				},
				{   
					id : 5,
					title: '도희동아백화점',
					latlng: new kakao.maps.LatLng(36.119735,128.3463003)
				},
				{   
					id : 6,
					title: '마지막',
					latlng: new kakao.maps.LatLng(36.119735,118.3463003)
				}
			]
		},
			
	// 	showNewMap(LatLng) { 
	// 		var map = this.map;
	// 		map.setCenter(LatLng);
	// 		var marker = new kakao.maps.Marker({ position: map.getCenter() });
	// 		marker.setMap(map);
	// 	},
			
	// 	showPositions(locs) {
	// 		var map = this.map;
	// 		var positions = locs;	
	// 		var imageSrc = "https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/markerStar.png"; 
	// 		var bounds = new kakao.maps.LatLngBounds();   
					
	// 		for (var i = 0; i < positions.length; i ++) {
					
	// 			// 마커 이미지의 이미지 크기 입니다
	// 			var imageSize = new kakao.maps.Size(24, 35); 
				
	// 			// 마커 이미지를 생성합니다    
	// 			var markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize); 
				
	// 			// 마커를 생성합니다
	// 			var marker = new kakao.maps.Marker({
	// 				map: map,
	// 				position: positions[i].latlng,
	// 				title : positions[i].title, 
	// 				image : markerImage
	// 			});

	// 			bounds.extend(positions[i].latlng);
	// 			marker.setMap(map);
	// 		}

	// 		// LatLngBounds 객체에 추가된 좌표들을 기준으로 지도의 범위를 재설정합니다
	// 		// 이때 지도의 중심좌표와 레벨이 변경될 수 있습니다
	// 		map.setBounds(bounds);	
	// 	},

		getTimeHTML(distance) {

			// 도보의 시속은 평균 4km/h 이고 도보의 분속은 67m/min
			var walkkTime = distance / 67 | 0;
			var walkHour = "", walkMin = "";

			// 계산한 도보 시간이 60분 보다 크면 시간으로 표시
			if (walkkTime > 60) {
				walkHour = '<span class="number">' + Math.floor(walkkTime / 60) + '</span>시간 '
			}
			walkMin = '<span class="number">' + walkkTime % 60 + '</span>분'

			// 자전거의 평균 시속은 16km/h 이고 이것을 기준으로 자전거의 분속은 267m/min
			var bycicleTime = distance / 227 | 0;
			var bycicleHour = '', bycicleMin = '';

			// 계산한 자전거 시간이 60분 보다 크면 시간으로 표출
			if (bycicleTime > 60) {
				bycicleHour = '<span class="number">' + Math.floor(bycicleTime / 60) + '</span>시간 '
			}
			bycicleMin = '<span class="number">' + bycicleTime % 60 + '</span>분'

			// KOSIS 통계청 국도 평일 평균 기준
			// 차 평균 시속 54km/h로 두고 분속 900m/min.
			// 300m마다 평균 2분씩 신호등 기다리기(정석) -> 신호를 지나치기 등등 고려(500미터당 1분) 
			// 이거는 나중에 변수값 조절해서 바꾸면 된다.
			var carTime = (distance / 900 | 0 ) + (distance / 500 | 0);
			var carHour = '', carMin = '';
			
			if (carTime > 60) {
				carHour = '<span class="number">' + Math.floor(carTime / 60) + '</span>시간 '
			}
			carMin = '<span class="number">' + carTime % 60 + '</span>분'

			// 거리와 도보 시간, 자전거 시간을 가지고 HTML Content를 만들어 리턴
			var content = '<ul class="dotOverlay distanceInfo">';
			content += '    <li>';
			content += '        <span class="label">총거리</span><span class="number">' + distance + '</span>m';
			content += '    </li>';
			content += '    <li>';
			content += '        <span class="label">도보</span>' + walkHour + walkMin;
			content += '    </li>';
			content += '    <li>';
			content += '        <span class="label">자전거</span>' + bycicleHour + bycicleMin;
			content += '    </li>';
			content += '    <li>';
			content += '        <span class="label">차</span>' + carHour + carMin;
			content += '    </li>';
			content += '</ul>'

			return content;
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

		
	// 	makePlan(position) {
	// 		var flag = true
	// 		this.plans.forEach(plan => {
	// 			if (position.id === plan.id){
	// 				flag = false
	// 				alert(`이미 ${position.title}은 일정에 있습니다.`)
	// 			}
	// 		});	
	// 		if (flag){
	// 			this.plans.push(position)
	// 		}
					
	// 		this.showPositions(this.plans)
	// 	},

	// 	resetPlans() {
	// 		this.plans = []
	// 		this.initMap()
	// 	},
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

#map {
	width: 400px;
	height: 500px;
	margin-left: auto;
	margin-right: auto;
}

</style>