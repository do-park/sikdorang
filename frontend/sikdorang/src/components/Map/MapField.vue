<template>
  <div>	
	<div class="map-wrap">
		<div id="map"></div>
	</div>
  </div>
</template>

<script>
// import swal from 'sweetalert';
import { mapGetters, mapActions } from "vuex"
import axios from "axios"

const kakaoMapKey = "d313fa70ad00838acce4a3b5bc134b23";

export default {
	name : "MapField",
	data() {
		return {
			destination : '',
			map: null,
			startLat :36.109328,
			startLong :128.4128223,
			startCoords : null,
			curLat: null,
			curLong: null,
			curMarkers : [],
			recommendMarkers : [],
			selectedMarker : null,
			plans : [],
			schedule : [],
			recommends : [],
			flip : false,
			clickedOverlay : null,
			// store에 저장하기 위해 올라가는 Index
			selectingIndex: 0,
			// 이전에 선택한 지점의 x , y 좌표
			beforeLng: null,
			beforeLat: null,
		}
	},
	mounted() {
		this.initCurLocation()
		if (window.kakao && window.kakao.map) {
			this.initMap();
		}
		else {
			this.addScript();
		}
		
	},
	computed : {
		...mapGetters("mapEvent", [
			'getFlip',
			'getMouseOver',
			'getClicked',
			'getThreeRes',
			'getSelectedRest',
			'getPlanList'
		]),
		...mapGetters("schedule", [
			"getSchedules",
			"getScheduleIdx",
		]),
	},
	watch : {
		getFlip(){
			this.changeThreeResByFlip()
			if (window.kakao) {
				this.showCandidates(this.recommends)
			}
		},
		selectedMarker(){
			this.$cookies.set('selectedMarker',this.selectedMarker.idx)
		},
		startCoords() {
			this.showCandidates(this.recommends)
		},
		recommends() {
			if (window.kakao && this.recommends) {
				this.showCandidates(this.recommends)
			}
		},
		getScheduleIdx() {
			if (this.getScheduleIdx < this.getSchedules.length)
			{
				// console.log(this.getScheduleIdx)
				// console.log(this.getSchedules[Number(this.getScheduleIdx)].name)
				this.divideRecommendation(this.getSchedules[Number(this.getScheduleIdx)].name)
				this.actionFlip(true)
				this.showCandidates(this.recommends)

			}
			else {
				this.$router.push('/mypage')
			}
			
		},
		

	},
	methods : {
		...mapActions("mapEvent",[
			'actionFlip',
			'actionMouseOver',
			'actionClicked',
			'actionThreeRes',
			'actionSelectedRest',
			'actionPlanList',
		]),
		...mapActions("schedule", [
			"actionStore"
		]),
		divideRecommendation(cf) {
			if (cf === "식당" | cf === "카페"){
				this.getSCRecommendation(cf)
			} else {
				this.getSHRecommendation(cf)
			}
		},
		getSCRecommendation(cf) {
            console.log('음식점 / 카페를 추천 받습니다.')
            this.recommends = []
            
			const requestHeaders = {
				headers: {
					Authorization: `JWT ${this.$cookies.get('auth-token')}`
				}
			}
			this.$axios.post('recommend/tag-recommend/', { category: cf, lat: this.beforeLat, lng: this.beforeLng }, requestHeaders)
			.then(res => {
				
				this.recommends = res.data.result
			
			})
			.catch(err => console.error("알고리즘 추천 실패야",err))
		},
		getSHRecommendation(cf) {
            console.log('관광지 / 숙박 정보를 받습니다.', cf)
            this.recommends = []
			const TOUR_API_KEY = "K%2FplKHR5Hx7sLQwMexw4LCgDz45JjMDfJ1czEyCx83EBoZHJLUOKe%2B56J93QhZ41DlYmdRy3b1LIpwlSh%2FxYfQ%3D%3D"
            let contentTypeId = 32
            if (cf ==="관광지") { contentTypeId = 12 }
            axios.get(`http://api.visitkorea.or.kr/openapi/service/rest/KorService/locationBasedList?ServiceKey=${TOUR_API_KEY}&contentTypeId=${contentTypeId}&mapX=${this.beforeLng}&mapY=${this.beforeLat}&radius=5000&listYN=Y&MobileOS=ETC&MobileApp=TourAPI3.0_Guide&arrange=A&numOfRows=12&pageNo=1&_type=json`)
            .then(res => {
                const items = res.data.response.body.items.item
                for (let i=0;i<items.length;i++) {
                    this.recommends.push({
                        "id": items[i].contentid,
                        "name": items[i].title,
                        "branch": "",
                        "tel": items[i].tel,
                        "address": items[i].addr1 + items[i].addr2,
                        "latitude": items[i].mapy,
                        "longtitude": items[i].mapx,
                        "category": "관광지",
                        "tags": "",
                        "img": items[i].firstimage,
                    })
                }
                // console.log(items)
            })
            .catch(err => console.error(err))
		},
		moveSmoothly() {
			// 이동할 위도 경도 위치를 생성합니다 
			if (this.getClicked) {
			
				var lat = this.getThreeRes[this.getClicked].latitude;
				var long = this.getThreeRes[this.getClicked].longtitude;
				var moveLatLon = new kakao.maps.LatLng(lat,long)

				// 지도 중심을 부드럽게 이동시킵니다
				// 만약 이동할 거리가 지도 화면보다 크면 부드러운 효과 없이 이동합니다
				this.map.panTo(moveLatLon);  
			}
		},
		initMap() { 
			var container = document.getElementById('map'); 
			var options = {
				center: new kakao.maps.LatLng(36.0970073,128.4254652),
				level: 3
			}; 
			var map = new kakao.maps.Map(container, options); 
            this.map = map;
			this.$emit('getKakao', window.kakao)

			this.startWithMap()
		},
		startWithMap() {
			this.setStartCoords();
			this.initCurLocation();
			this.divideRecommendation(this.getSchedules[Number(this.getScheduleIdx)].name)
			this.showCandidates(this.recommends)
		},
		initCurLocation() {
			this.curLat = this.startLat
			this.curLong = this.startLong
			this.beforeLng = this.$cookies.get("startLongitude")
			this.beforeLat = this.$cookies.get("startLatitude")
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
	
		// "마커 보이기" 버튼을 클릭하면 호출되어 배열에 추가된 마커를 지도에 표시하는 함수입니다
		showMarkers(markers) {
			for (var i = 0; i < markers.length; i++) {
				markers[i].setMap(this.map);
			}    
		},

		// "마커 감추기" 버튼을 클릭하면 호출되어 배열에 추가된 마커를 지도에서 삭제하는 함수입니다
		hideMarkers(markers) {
			for (var i = 0; i < markers.length; i++) {
				markers[i].setMap(null);
			} 
		},

        async setStartCoords() {
			var map = this.map
			
            if (this.$cookies.get("searchMethod")==="myLocation"){
            this.startLat = this.$cookies.get("startLatitude")
            this.startLong = this.$cookies.get("startLongitude")

            this.startCoords = new kakao.maps.LatLng(this.startLat, this.startLong)
            map.setCenter(this.startCoords);
			var marker = new kakao.maps.Marker({ position: map.getCenter() });
			this.hideMarkers(this.curMarkers)
			this.curMarkers = [];
			
			// 마커를 추가
			this.curMarkers.push(marker);
			this.showMarkers(this.curMarkers);

            }
            else {
                this.destination = this.$cookies.get('destination')

                // 주소-좌표 변환 객체를 생성합니다
                var geocoder = new kakao.maps.services.Geocoder();

                // 주소로 좌표를 검색합니다
                await geocoder.addressSearch(this.destination, (result, status) => {

                    // 정상적으로 검색이 완료됐으면 
                    if (status === kakao.maps.services.Status.OK) {
						this.startCoords = new kakao.maps.LatLng(result[0].y, result[0].x);
						this.startLat = result[0].y
						this.startLong = result[0].x

                        // 지도의 중심을 결과값으로 받은 위치로 이동시킵니다
						map.setCenter(this.startCoords);
						// console.log(`${this.destination} 좌표 : ${this.startCoords} `)
                        var marker = new kakao.maps.Marker({ position: map.getCenter() });
					
						// 마커를 추가
						this.hideMarkers(this.curMarkers)
						this.curMarkers = [];
						this.curMarkers.push(marker);
						this.showMarkers(this.curMarkers);
					} 
					else{
						console.log("검색 결과 오류입니다.")
					}
					this.changeThreeResByFlip()
                })
            }
		},
		changeThreeResByFlip() {
			
			if (this.getFlip) {
				this.actionThreeRes(this.recommends.slice(0,3))
			}
			else {
				this.actionThreeRes(this.recommends.slice(3))
			}
		},
		fillPositions() {
			this.recommends = [
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
					title: '인동스타벅스',
					latlng: new kakao.maps.LatLng(36.1073795,128.4174558)
				}
			]
		},
		// selectRest(idx) {
		// 	this.actionSelectedRest(this.getThreeRes[idx])
		// 	const self = this
        //     var Rest = this.getSelectedRest
        //     swal({
		// 		title: Rest.title,
		// 		text: "이런이런 맛집입니다아",
		// 		buttons: ["취소","추가"],
        //     })
        //     .then((res) => {
		// 		if (res) {
		// 			swal(`${Rest.title}을 일정에 추가할까요?`,{
		// 				buttons: ["아니오","네"],
		// 			})
		// 			.then((res)=>{
		// 				if (res) {
		// 					swal(`${Rest.title}을 일정에 추가할까요?`,{
		// 						icon : "success"
		// 					})
		// 					// store에 올리는 로직.
		// 					self.actionStore({ store: Rest,  index: self.selectingIndex })
		// 					self.selectingIndex += 1
		// 					self.beforeLng = Rest.lng
		// 					self.beforeLat = Rest.lat
		// 				}
		// 			})
		// 		} 
		// 	});
		// },

		//카드 누르면 마커 이미지 변경
		clickCardChangeMarker(marker, normalImage, overImage,clickImage) {

			if (this.getClicked !== marker.idx) {
				marker.setImage(normalImage);
			}
			else {
				this.selectedMarker = marker;
				marker.setImage(clickImage);
			}
			return this.selectedMarker	
		},
        
		showCandidates(locs) {

			const self = this
			var map = this.map;
			if (this.getFlip) {
				this.actionThreeRes(locs.slice(0,3))
			}
			else {
				this.actionThreeRes(locs.slice(3,6))
			}
			var positions = this.getThreeRes;
			var bounds = new kakao.maps.LatLngBounds();

			//현재 위치도 지도 범위에 포함  
			bounds.extend(self.startCoords);

			this.hideMarkers(this.recommendMarkers)
			this.recommendMarkers = [];

			//커스텀 마커 정보
			var MARKER_WIDTH = 33, // 기본, 클릭 마커의 너비
				MARKER_HEIGHT = 36, // 기본, 클릭 마커의 높이
				OFFSET_X = 12, // 기본, 클릭 마커의 기준 X좌표
				OFFSET_Y = MARKER_HEIGHT, // 기본, 클릭 마커의 기준 Y좌표
				OVER_MARKER_WIDTH = 40, // 오버 마커의 너비
				OVER_MARKER_HEIGHT = 42, // 오버 마커의 높이
				OVER_OFFSET_X = 13, // 오버 마커의 기준 X좌표
				OVER_OFFSET_Y = OVER_MARKER_HEIGHT, // 오버 마커의 기준 Y좌표
				SPRITE_GAP = 10; // 스프라이트 이미지에서 마커간 간격
		

			var markerSize = new kakao.maps.Size(MARKER_WIDTH, MARKER_HEIGHT), // 기본, 클릭 마커의 크기
				markerOffset = new kakao.maps.Point(OFFSET_X, OFFSET_Y), // 기본, 클릭 마커의 기준좌표
				overMarkerSize = new kakao.maps.Size(OVER_MARKER_WIDTH, OVER_MARKER_HEIGHT), // 오버 마커의 크기
				overMarkerOffset = new kakao.maps.Point(OVER_OFFSET_X, OVER_OFFSET_Y); // 오버 마커의 기준 좌표
			
			// 클릭한 마커를 담을 변수
			var selectedMarker = this.selectedMarker;	

			for (var i = 0; i < positions.length; i ++) {
				const gapX = (MARKER_WIDTH + SPRITE_GAP), // 스프라이트 이미지에서 마커로 사용할 이미지 X좌표 간격 값
					originY = (MARKER_HEIGHT + SPRITE_GAP) * i, // 스프라이트 이미지에서 기본, 클릭 마커로 사용할 Y좌표 값
					overOriginY = (OVER_MARKER_HEIGHT + SPRITE_GAP) * i, // 스프라이트 이미지에서 오버 마커로 사용할 Y좌표 값
					normalOrigin = new kakao.maps.Point(0, originY), // 스프라이트 이미지에서 기본 마커로 사용할 영역의 좌상단 좌표
					clickOrigin = new kakao.maps.Point(gapX, originY), // 스프라이트 이미지에서 마우스오버 마커로 사용할 영역의 좌상단 좌표
					overOrigin = new kakao.maps.Point(gapX * 2, overOriginY); // 스프라이트 이미지에서 클릭 마커로 사용할 영역의 좌상단 좌표

				
				// 기본 마커이미지, 오버 마커이미지, 클릭 마커이미지를 생성합니다
				const normalImage = this.createMarkerImage(markerSize, markerOffset, normalOrigin),
					overImage = this.createMarkerImage(overMarkerSize, overMarkerOffset, overOrigin),
					clickImage = this.createMarkerImage(markerSize, markerOffset, clickOrigin);

				var position = new kakao.maps.LatLng(positions[i].latitude, positions[i].longtitude);
					
				// 마커를 생성합니다
				const marker = new kakao.maps.Marker({
					map: map,
					position: position,
					title : positions[i].name, 
					image : normalImage
				});

				marker.normalImage = normalImage;
				marker.idx = i;

				// 마커에 표시할 인포윈도우를 생성합니다 
				var infowindow = new kakao.maps.InfoWindow({
					content: positions[i].name // 인포윈도우에 표시할 내용
				});

				kakao.maps.event.addListener(marker, 'mouseover', makeOverListener(map, marker,infowindow,overImage));
				kakao.maps.event.addListener(marker, 'mouseout', makeOutListener(map, marker,infowindow,normalImage));
				kakao.maps.event.addListener(marker, 'click', makeClickListener(map, marker,infowindow,clickImage));
		
				//지도 범위에 추가
				bounds.extend(position);
				this.recommendMarkers.push(marker)
				selectedMarker = self.clickCardChangeMarker(marker, normalImage,overImage,clickImage)
			}
			function makeOverListener(map, marker, infowindow, overImage) {
				return function() {
					infowindow.open(map, marker);
					if (!selectedMarker || selectedMarker !== marker) {
						marker.setImage(overImage);
					}
					self.actionMouseOver(marker.idx)
				};
			}
			function makeOutListener(map, marker,infowindow,normalImage) {
				return function() {
					infowindow.close();
					//클릭된 마커가 없고, mouseout된 마커가 클릭된 마커가 아니면
					// 마커의 이미지를 기본 이미지로 변경합니다
					if (!selectedMarker || selectedMarker !== marker) {
						marker.setImage(normalImage);
					}
					self.actionMouseOver(null);
				};
			}
			function makeClickListener(map, marker, infowindow, clickImage) {
				
				return function() {
					//클릭된 마커가 없고, click 마커가 클릭된 마커가 아니면
					// 마커의 이미지를 클릭 이미지로 변경합니다
					if (!selectedMarker || selectedMarker !== marker) {
							// 클릭된 마커 객체가 null이 아니면
							// 클릭된 마커의 이미지를 기본 이미지로 변경하고
							!!selectedMarker && selectedMarker.setImage(selectedMarker.normalImage);

							// 현재 클릭된 마커의 이미지는 클릭 이미지로 변경합니다
							marker.setImage(clickImage);
						// }
						
					}

					// 클릭된 마커를 현재 클릭된 마커 객체로 설정합니다
					selectedMarker = marker;
					this.selectedMarker = selectedMarker;
					infowindow.close();
					window.$cookies.set('selectedMarker', selectedMarker.idx)
					self.actionClicked(selectedMarker.idx)
					// self.selectRest(selectedMarker.idx)
					
				};
			}

			// LatLngBounds 객체에 추가된 좌표들을 기준으로 지도의 범위를 재설정합니다
			// 이때 지도의 중심좌표와 레벨이 변경될 수 있습니다
			map.setBounds(bounds);
			this.showMarkers(this.recommendMarkers);
			self.moveSmoothly();
		},	
	
		// MakrerImage 객체를 생성하여 반환하는 함수입니다
		createMarkerImage(markerSize, offset, spriteOrigin) {
			var SPRITE_MARKER_URL = 'https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/markers_sprites2.png' // 스프라이트 마커 이미지 URL
			var SPRITE_WIDTH = 126, // 스프라이트 이미지 너비
				SPRITE_HEIGHT = 146 // 스프라이트 이미지 높이
			var	spriteImageSize = new kakao.maps.Size(SPRITE_WIDTH, SPRITE_HEIGHT); // 스프라이트 이미지의 크기
			
			var markerImage = new kakao.maps.MarkerImage(
				SPRITE_MARKER_URL, // 스프라이트 마커 이미지 URL
				markerSize, // 마커의 크기
				{
					offset: offset, // 마커 이미지에서의 기준 좌표
					spriteOrigin: spriteOrigin, // 스트라이프 이미지 중 사용할 영역의 좌상단 좌표
					spriteSize: spriteImageSize // 스프라이트 이미지의 크기
				}
			);
			
			return markerImage;
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
	}, 
}
</script>

<style scoped>

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