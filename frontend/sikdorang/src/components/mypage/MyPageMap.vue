<template>
  <div>	
	<div class="map-wrap">
		<div id="map"></div>
	</div>
  </div>
</template>

<script>
// import swal from 'sweetalert';
// import { mapGetters, mapActions } from "vuex"

const kakaoMapKey = "d313fa70ad00838acce4a3b5bc134b23";

export default {
	name : "MyPageMap",
	data() {
		return {
			curPath: [],
			plans : [],
		}
	},
	props: {
		todaySchedule: Array,
	},
	mounted() {
		this.addScript()
		// this.divideRecommendation(this.getSchedules[Number(this.getScheduleIdx)].name)
	},
	watch : {
		todaySchedule() {
			this.plans = this.todaySchedule
		}
	},
	methods : {
		moveSmoothly(cd) {
			// 이동할 위도 경도 위치를 생성합니다 
		var lat = null,
			long = null;
			if (cd === 'over' && this.getMouseOver !== null) {
				lat = this.getThreeRes[this.getMouseOver].latitude
				long = this.getThreeRes[this.getMouseOver].longitude
			} else if (cd === 'click' && this.getClicked !== null) {
				lat = this.getThreeRes[this.getClicked].latitude
				long = this.getThreeRes[this.getClicked].longitude
			} else if (cd === 'progress' && this.getProgressClicked !== null) {
				try {
					lat = this.getSchedules[this.getScheduleProgressIdx].userChoice.latitude
					long = this.getSchedules[this.getScheduleProgressIdx].userChoice.longitude
				} catch (err) {
					lat = this.beforeLat
					long = this.beforeLng
				}
			}
			let moveLatLon = new kakao.maps.LatLng(lat,long)
			this.map.panTo(moveLatLon);
			this.actionscheduleProgressIdx(-1)
		},
		initMap() { 
			var container = document.getElementById('map'); 
			var options = {
				center: new kakao.maps.LatLng(36.0970073,128.4254652),
				level: 3
			}; 
			var map = new kakao.maps.Map(container, options); 
            this.map = map;
			this.showPaths()
			
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
			var content = '<ul style="list-style:none; color:black; font-weight: bold;" class="dotOverlay distanceInfo">';
			content += '    <li>';
			content += '        <span class="label">거리</span><span class="number">' + distance + '</span>m';
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
			var imageSrc = "https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/markerStar.png"; 
			var bounds = new kakao.maps.LatLngBounds();
			
			plans.forEach(plan => {
				var position = new kakao.maps.LatLng(plan.latitude, plan.longitude)
				plan.latlng = position
				bounds.extend(position);

			})
			if (this.curPath.length) {
				for (let i=0; i<this.curPath.length; i++) {
					this.curPath[i].setMap(null)
				}
			}
			for (var i = 1; i < plans.length; i ++) {	
				var linePath = [
					plans[i-1].latlng,
					plans[i].latlng 
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
				this.curPath.push(polyline)
				polyline.setMap(map); 
				var distance = Math.round(polyline.getLength());
				var content = this.getTimeHTML(distance);

				// 커스텀 오버레이를 생성하고 지도에 표시합니다
				var distanceOverlay = new kakao.maps.CustomOverlay({
					map: map, // 커스텀오버레이를 표시할 지도입니다
					content: content,  // 커스텀오버레이에 표시할 내용입니다
					position: plans[i].latlng, // 커스텀오버레이를 표시할 위치입니다.
					xAnchor: 0,
					yAnchor: 0,
					zIndex: 3  
				}); 
				this.curPath.push(distanceOverlay)
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
					title : plan.store_name,
					image : markerImage
				});
				var infowindow = new kakao.maps.InfoWindow({
					content: `<h5>${plan.store_name}</h5>` // 인포윈도우에 표시할 내용
				});
			var OVER_MARKER_WIDTH = 27, // 오버 마커의 너비
				OVER_MARKER_HEIGHT = 42 // 오버 마커의 높이
			var overMarkerSize = new kakao.maps.Size(OVER_MARKER_WIDTH, OVER_MARKER_HEIGHT) // 오버 마커의 크기
				const overImage = new kakao.maps.MarkerImage(imageSrc, overMarkerSize); 

				kakao.maps.event.addListener(marker, 'mouseover', makeOverListener(map, marker,infowindow,overImage))
				kakao.maps.event.addListener(marker, 'mouseout', makeOutListener(map, marker,infowindow,markerImage))

				let selectedMarker = this.selectedMarker
				// const self = this
				function makeOverListener(map, marker, infowindow, overImage) {
					return function() {
						infowindow.open(map, marker);
						if (!selectedMarker || selectedMarker !== marker) {
							marker.setImage(overImage);
						}
					};
				}
				function makeOutListener(map, marker,infowindow, normalImage) {
					return function() {
						infowindow.close();
						//클릭된 마커가 없고, mouseout된 마커가 클릭된 마커가 아니면
						// 마커의 이미지를 기본 이미지로 변경합니다
						if (!selectedMarker || selectedMarker !== marker) {
							marker.setImage(normalImage);
						}
					};
				}
				marker.setMap(map);

			})
			map.setBounds(bounds);
		},
	},
}

</script>

<style scoped>
#map {
	width: 100%;
	height: 200px;
	margin: 0.5rem auto;
}
</style>
