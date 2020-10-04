<template>
  <div>
    <div class="map-wrap">
      <div id="map"></div>
    </div>
  </div>
</template>

<script>
// import swal from 'sweetalert';
import { mapGetters, mapActions } from "vuex";
import axios from "axios";

const kakaoMapKey = "d313fa70ad00838acce4a3b5bc134b23";

export default {
	name : "MapField",
	data() {
		return {
			destination : '',
			map: null,
			startLat : null,
			startLong : null,
			startCoords : null,
			curLat: null,
			curLong: null,
			curMarkers : [],
			curPath: [],
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
		this.addScript()
		this.actionMapEventClear()
		// this.divideRecommendation(this.getSchedules[Number(this.getScheduleIdx)].name)
	},
	computed : {
		...mapGetters("mapEvent", [
			'getFlip',
			'getMouseOver',
			'getClicked',
			'getThreeRes',
			'getSelectedRest',
			'getPlanList',
			'getSelectTag',
			'getTagStores',
		]),
		...mapGetters("schedule", [
			"getSchedules",
			"getScheduleIdx",
			"getScheduleProgressIdx",
			"getBeforeCat",
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
		getScheduleIdx() {
			if (this.getScheduleIdx < this.getSchedules.length){
				this.actionFlip(true)
				this.beforeLng = this.getSchedules[Number(this.getScheduleIdx)-1].userChoice.longitude
				this.beforeLat = this.getSchedules[Number(this.getScheduleIdx)-1].userChoice.latitude
				this.divideRecommendation(this.getSchedules[Number(this.getScheduleIdx)].name)
			} else {
				this.$router.replace('/mypage')
			}
		},
		getPlanList() {
			if (this.getPlanList.length !== 0) {
				this.showPaths()
			}
		},
		getMouseOver() {
			if (this.getMouseOver !== null) {
				if (this.getTagStores) {
					this.moveTagSmoothly('over')
				} else {
					this.moveSmoothly('over')
				}
			}
		},
		getClicked() {
			if (this.getClicked !== null) {
				if (this.getTagStores) {
					this.moveTagSmoothly('click')
				} else {
					this.moveSmoothly('click')
				}
			}
		},
		getScheduleProgressIdx() {
			if (this.getScheduleProgressIdx !== -1){
				this.moveSmoothly('progress')
			}
		},
		getSelectTag() {
			if (this.getSelectTag !== null){
				this.getTagStoreList(this.getSelectTag)
			}
		},
	},
	methods : {
		...mapActions("mapEvent",[
			'actionFlip',
			'actionMouseOver',
			'actionMouseOverToCard',
			'actionClicked',
			'actionThreeRes',
			'actionMapEventClear',
			'actionSelectedRest',
			'actionPlanList',
			'actionTags',
			'actionTagStores',
		]),
		...mapActions("schedule", [
			"actionStore",
			"actionscheduleProgressIdx",
		]),
		getTagStoreList(tag){
			const data = {
				"tag": tag,
				"lat": this.beforeLat,
				"lng": this.beforeLng,
			}
			this.$axios.post('recommend/tag-store/', data)
			.then(res => {
				this.showTagStores(res.data.result)
				this.actionTagStores(res.data.result)
			})
			.catch(err => console.error(err))
		},
		divideRecommendation(cf) {
			this.recommends = []
			this.actionTags([])
			if (cf === "식당" | cf === "카페"){
				this.getSCRecommendation(cf)
			} else {
				this.getSHRecommendation(cf)
			}
		},
		getSCRecommendation(cf) {
			const requestHeaders = {
				headers: {
					Authorization: `JWT ${this.$cookies.get('auth-token')}`
				}
			}
			this.$axios.post('recommend/tag-recommend/', { category: cf, lat: this.beforeLat, lng: this.beforeLng, bc: this.getBeforeCat }, requestHeaders)
			.then(res => {
				this.actionTags(res.data.tags)
				this.recommends = res.data.result
				this.showCandidates(this.recommends)
			})
			.catch(err => console.error("알고리즘 추천 실패",err))
		},
		getSHRecommendation(cf) {
			const TOUR_API_KEY = this.$store.state.TOUR_API_KEY
            let contentTypeId = 32
            if (cf ==="관광지") { contentTypeId = 12 }
            axios.get(`http://api.visitkorea.or.kr/openapi/service/rest/KorService/locationBasedList?ServiceKey=${TOUR_API_KEY}&contentTypeId=${contentTypeId}&mapX=${this.beforeLng}&mapY=${this.beforeLat}&radius=5000&listYN=Y&MobileOS=ETC&MobileApp=TourAPI3.0_Guide&arrange=A&numOfRows=12&pageNo=1&_type=json`)
            .then(res => {
				const items = res.data.response.body.items.item
                for (let i=0;i<items.length;i++) {
					let address = null
					if (typeof(items[i].addr2) !== "undefined") {
						address = items[i].addr1 + items[i].addr2
					} else {
						address = items[i].addr1
					}
                    this.recommends.push({
                        "id": items[i].contentid,
                        "name": items[i].title,
                        "branch": "",
                        "tel": items[i].tel,
                        "address": address,
                        "latitude": items[i].mapy,
                        "longitude": items[i].mapx,
                        "category": cf,
                        "tags": "",
                        "img": items[i].firstimage,
                    })
				}
				this.showCandidates(this.recommends, '관광/숙박')
            })
            .catch(err => console.error(err))
		},
		moveTagSmoothly(cd) {
		var lat = null,
			long = null;
			if (cd === 'over' && this.getMouseOver !== null) {
				lat = this.getTagStores[this.getMouseOver].latitude
				long = this.getTagStores[this.getMouseOver].longitude
			} else if (cd === 'click' && this.getClicked !== null) {
				lat = this.getTagStores[this.getClicked].latitude
				long = this.getTagStores[this.getClicked].longitude
			}
			let moveLatLon = new kakao.maps.LatLng(lat,long)
			this.map.panTo(moveLatLon);
		},
		moveSmoothly(cd) {
			// 이동할 위도 경도 위치를 생성합니다 
		var lat = null,
			long = null;
			if (cd === 'over' && this.getMouseOver !== null) {
				console.log(123)
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
			this.$emit('getKakao', window.kakao)
			this.setStartCoords();

		},
		initCurLocation() {
			this.curLat = this.startLat
			this.curLong = this.startLong
			this.beforeLng = this.startLong
			this.beforeLat = this.startLat
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

        setStartCoords() {
			var map = this.map
			this.showPaths()
            if (this.$cookies.get("searchMethod")==="myLocation"){
				this.startLat = this.$cookies.get("startLatitude")
				this.startLong = this.$cookies.get("startLongitude")
				this.initCurLocation()
				this.divideRecommendation(this.getSchedules[Number(this.getScheduleIdx)].name)
				this.startCoords = new kakao.maps.LatLng(this.startLat, this.startLong)
				map.setCenter(this.startCoords);
				var marker = new kakao.maps.Marker({ position: map.getCenter() });
				this.hideMarkers(this.curMarkers)
				this.curMarkers = [];
				
				// 마커를 추가
				this.curMarkers.push(marker);
				this.showMarkers(this.curMarkers);
            }
            this.recommends.push({
              id: items[i].contentid,
              name: items[i].title,
              branch: "",
              tel: items[i].tel,
              address: address,
              latitude: items[i].mapy,
              longitude: items[i].mapx,
              category: cf,
              tags: "",
              img: items[i].firstimage,
            });
          }
          this.showCandidates(this.recommends, "관광/숙박");
        })
        .catch((err) => console.error(err));
    },
    moveTagSmoothly(cd) {
      var lat = null,
        long = null;
      if (cd === "over" && this.getMouseOver !== null) {
        lat = this.getTagStores[this.getMouseOver].latitude;
        long = this.getTagStores[this.getMouseOver].longitude;
      } else if (cd === "click" && this.getClicked !== null) {
        lat = this.getTagStores[this.getClicked].latitude;
        long = this.getTagStores[this.getClicked].longitude;
      }
      let moveLatLon = new kakao.maps.LatLng(lat, long);
      this.map.panTo(moveLatLon);
    },
    moveSmoothly(cd) {
      // 이동할 위도 경도 위치를 생성합니다
      var lat = null,
        long = null;
      if (cd === "over" && this.getMouseOver !== null) {
        console.log(123);
        lat = this.getThreeRes[this.getMouseOver].latitude;
        long = this.getThreeRes[this.getMouseOver].longitude;
      } else if (cd === "click" && this.getClicked !== null) {
        lat = this.getThreeRes[this.getClicked].latitude;
        long = this.getThreeRes[this.getClicked].longitude;
      } else if (cd === "progress" && this.getProgressClicked !== null) {
        try {
          lat = this.getSchedules[this.getScheduleProgressIdx].userChoice
            .latitude;
          long = this.getSchedules[this.getScheduleProgressIdx].userChoice
            .longitude;
        } catch (err) {
          lat = this.beforeLat;
          long = this.beforeLng;
        }
      }
      let moveLatLon = new kakao.maps.LatLng(lat, long);
      this.map.panTo(moveLatLon);
      this.actionscheduleProgressIdx(-1);
    },
    initMap() {
      var container = document.getElementById("map");
      var options = {
        center: new kakao.maps.LatLng(36.0970073, 128.4254652),
        level: 3,
      };
      var map = new kakao.maps.Map(container, options);
      this.map = map;
      this.$emit("getKakao", window.kakao);
      this.setStartCoords();
    },
    initCurLocation() {
      this.curLat = this.startLat;
      this.curLong = this.startLong;
      this.beforeLng = this.startLong;
      this.beforeLat = this.startLat;
    },
    //cdn 추가
    addScript() {
      const script1 = document.createElement("script"); // 지우면 작동안함
      /* global kakao */ script1.src = `http://dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=${kakaoMapKey}`;
      document.head.appendChild(script1);

      const script2 = document.createElement("script");
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

    setStartCoords() {
      var map = this.map;
      this.showPaths();
      if (this.$cookies.get("searchMethod") === "myLocation") {
        this.startLat = this.$cookies.get("startLatitude");
        this.startLong = this.$cookies.get("startLongitude");
        this.initCurLocation();
        this.divideRecommendation(
          this.getSchedules[Number(this.getScheduleIdx)].name
        );
        this.startCoords = new kakao.maps.LatLng(this.startLat, this.startLong);
        map.setCenter(this.startCoords);
        var marker = new kakao.maps.Marker({ position: map.getCenter() });
        this.hideMarkers(this.curMarkers);
        this.curMarkers = [];

        // 마커를 추가
        this.curMarkers.push(marker);
        this.showMarkers(this.curMarkers);
      } else {
        this.destination = this.$cookies.get("destination");
        // 주소-좌표 변환 객체를 생성합니다
        var geocoder = new kakao.maps.services.Geocoder();
        // 주소로 좌표를 검색합니다
        geocoder.addressSearch(this.destination, (result, status) => {
          // 정상적으로 검색이 완료됐으면
          if (status === kakao.maps.services.Status.OK) {
            this.startCoords = new kakao.maps.LatLng(result[0].y, result[0].x);
            this.startLat = result[0].y;
            this.startLong = result[0].x;
            this.initCurLocation();
            this.divideRecommendation(
              this.getSchedules[Number(this.getScheduleIdx)].name
            );

            // 지도의 중심을 결과값으로 받은 위치로 이동시킵니다
            map.setCenter(this.startCoords);
            var marker = new kakao.maps.Marker({ position: map.getCenter() });

            // 마커를 추가
            this.hideMarkers(this.curMarkers);
            this.curMarkers = [];
            this.curMarkers.push(marker);
            this.showMarkers(this.curMarkers);
          } else {
            console.error("검색 결과 오류입니다.");
          }
          this.changeThreeResByFlip();
        });
      }
    },
    changeThreeResByFlip() {
      if (this.getFlip) {
        this.actionThreeRes(this.recommends.slice(0, 3));
      } else {
        this.actionThreeRes(this.recommends.slice(3));
        if (this.getThreeRes.length === 0) {
          this.actionThreeRes(this.recommends.slice(0, 3));
        }
      }
    },
    //카드 누르면 마커 이미지 변경
    clickCardChangeMarker(marker, normalImage, overImage, clickImage) {
      if (this.getClicked !== marker.idx) {
        marker.setImage(normalImage);
      } else {
        this.selectedMarker = marker;
        marker.setImage(clickImage);
      }
      return this.selectedMarker;
    },
    showTagStores(stores) {
      const map = this.map;
      const self = this;
      this.actionClicked(null);
      this.hideMarkers(this.recommendMarkers);
      this.recommendMarkers = [];
      var bounds = new kakao.maps.LatLngBounds();

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
        overMarkerSize = new kakao.maps.Size(
          OVER_MARKER_WIDTH,
          OVER_MARKER_HEIGHT
        ), // 오버 마커의 크기
        overMarkerOffset = new kakao.maps.Point(OVER_OFFSET_X, OVER_OFFSET_Y); // 오버 마커의 기준 좌표

      // 클릭한 마커를 담을 변수
      var selectedMarker = this.selectedMarker;
      for (var i = 0; i < stores.length; i++) {
        const gapX = MARKER_WIDTH + SPRITE_GAP, // 스프라이트 이미지에서 마커로 사용할 이미지 X좌표 간격 값
          originY = MARKER_HEIGHT + SPRITE_GAP, // 스프라이트 이미지에서 기본, 클릭 마커로 사용할 Y좌표 값
          overOriginY = OVER_MARKER_HEIGHT + SPRITE_GAP, // 스프라이트 이미지에서 오버 마커로 사용할 Y좌표 값
          normalOrigin = new kakao.maps.Point(0, originY), // 스프라이트 이미지에서 기본 마커로 사용할 영역의 좌상단 좌표
          clickOrigin = new kakao.maps.Point(gapX, originY), // 스프라이트 이미지에서 마우스오버 마커로 사용할 영역의 좌상단 좌표
          overOrigin = new kakao.maps.Point(gapX * 2, overOriginY); // 스프라이트 이미지에서 클릭 마커로 사용할 영역의 좌상단 좌표

        // 기본 마커이미지, 오버 마커이미지, 클릭 마커이미지를 생성합니다
        const normalImage = this.createMarkerImage(
            markerSize,
            markerOffset,
            normalOrigin
          ),
          overImage = this.createMarkerImage(
            overMarkerSize,
            overMarkerOffset,
            overOrigin
          ),
          clickImage = this.createMarkerImage(
            markerSize,
            markerOffset,
            clickOrigin
          );

        var position = new kakao.maps.LatLng(
          stores[i].latitude,
          stores[i].longitude
        );

        // 마커를 생성합니다
        const marker = new kakao.maps.Marker({
          map: map,
          position: position,
          title: stores[i].name,
          image: normalImage,
        });

        marker.normalImage = normalImage;
        marker.idx = i;

        // 마커에 표시할 인포윈도우를 생성합니다
        var infowindow = new kakao.maps.InfoWindow({
          content: `<div style="width:150px;text-align:center;padding:6px 0;">${stores[i].name}</div>`, // 인포윈도우에 표시할 내용
        });

        kakao.maps.event.addListener(
          marker,
          "mouseover",
          makeOverListener(map, marker, infowindow, overImage)
        );
        kakao.maps.event.addListener(
          marker,
          "mouseout",
          makeOutListener(map, marker, infowindow, normalImage)
        );
        kakao.maps.event.addListener(
          marker,
          "click",
          makeClickListener(map, marker, infowindow, clickImage)
        );

        //지도 범위에 추가
        bounds.extend(position);
        this.recommendMarkers.push(marker);
        // selectedMarker = self.clickCardChangeMarker(marker, normalImage,overImage,clickImage)
      }
      function makeOverListener(map, marker, infowindow, overImage) {
        return function() {
          infowindow.open(map, marker);
          if (!selectedMarker || selectedMarker !== marker) {
            marker.setImage(overImage);
          }
          // self.actionMouseOverToCard(marker.idx)
        };
      }
      function makeOutListener(map, marker, infowindow, normalImage) {
        return function() {
          infowindow.close();
          //클릭된 마커가 없고, mouseout된 마커가 클릭된 마커가 아니면
          // 마커의 이미지를 기본 이미지로 변경합니다
          if (!selectedMarker || selectedMarker !== marker) {
            marker.setImage(normalImage);
          }
          // self.actionMouseOverToCard(null);
        };
      }
      function makeClickListener(map, marker, infowindow, clickImage) {
        return function() {
          //클릭된 마커가 없고, click 마커가 클릭된 마커가 아니면
          // 마커의 이미지를 클릭 이미지로 변경합니다
          if (!selectedMarker || selectedMarker !== marker) {
            // 클릭된 마커 객체가 null이 아니면
            // 클릭된 마커의 이미지를 기본 이미지로 변경하고
            !!selectedMarker &&
              selectedMarker.setImage(selectedMarker.normalImage);

            // 현재 클릭된 마커의 이미지는 클릭 이미지로 변경합니다
            marker.setImage(clickImage);
            // }
          }
          // 클릭된 마커를 현재 클릭된 마커 객체로 설정합니다
          selectedMarker = marker;
          this.selectedMarker = selectedMarker;
          infowindow.close();
          window.$cookies.set("selectedMarker", selectedMarker.idx);
          console.log(selectedMarker.idx);
          self.actionClicked(selectedMarker.idx);
          // self.selectRest(selectedMarker.idx)
        };
      }

      map.setBounds(bounds);
      this.showMarkers(this.recommendMarkers);
    },
    getRandomInt(min, max) {
      min = Math.ceil(min);
      max = Math.floor(max);
      return Math.floor(Math.random() * (max - min)) + min; //최댓값은 제외, 최솟값은 포함
    },
    showCandidates(locs, cf = null) {
      const self = this;
      var map = this.map;
      this.actionClicked(null);
      let ranIdx = [];
      let positions = [];
      if (cf !== null) {
        while (ranIdx.length < 6 && ranIdx.length < locs.length) {
          let idx = this.getRandomInt(0, locs.length);
          if (ranIdx.indexOf(idx) === -1) {
            ranIdx.push(idx);
          }
        }
        positions = locs.filter((el, index) => {
          return ranIdx.indexOf(index) !== -1;
        });
        if (this.getFlip) {
          this.actionThreeRes(positions.slice(0, 3));
        } else {
          this.actionThreeRes(positions.slice(3, 6));
        }
      } else {
        if (this.getFlip) {
          this.actionThreeRes(locs.slice(0, 3));
        } else {
          this.actionThreeRes(locs.slice(3, 6));
        }
        positions = this.getThreeRes;
      }
      if (positions.length === 0) {
        return;
      }
      var bounds = new kakao.maps.LatLngBounds();

      //현재 위치도 지도 범위에 포함
      bounds.extend(self.startCoords);

      this.hideMarkers(this.recommendMarkers);
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
        overMarkerSize = new kakao.maps.Size(
          OVER_MARKER_WIDTH,
          OVER_MARKER_HEIGHT
        ), // 오버 마커의 크기
        overMarkerOffset = new kakao.maps.Point(OVER_OFFSET_X, OVER_OFFSET_Y); // 오버 마커의 기준 좌표

      // 클릭한 마커를 담을 변수
      var selectedMarker = this.selectedMarker;

      for (var i = 0; i < positions.length; i++) {
        const gapX = MARKER_WIDTH + SPRITE_GAP, // 스프라이트 이미지에서 마커로 사용할 이미지 X좌표 간격 값
          originY = (MARKER_HEIGHT + SPRITE_GAP) * i, // 스프라이트 이미지에서 기본, 클릭 마커로 사용할 Y좌표 값
          overOriginY = (OVER_MARKER_HEIGHT + SPRITE_GAP) * i, // 스프라이트 이미지에서 오버 마커로 사용할 Y좌표 값
          normalOrigin = new kakao.maps.Point(0, originY), // 스프라이트 이미지에서 기본 마커로 사용할 영역의 좌상단 좌표
          clickOrigin = new kakao.maps.Point(gapX, originY), // 스프라이트 이미지에서 마우스오버 마커로 사용할 영역의 좌상단 좌표
          overOrigin = new kakao.maps.Point(gapX * 2, overOriginY); // 스프라이트 이미지에서 클릭 마커로 사용할 영역의 좌상단 좌표

        // 기본 마커이미지, 오버 마커이미지, 클릭 마커이미지를 생성합니다
        const normalImage = this.createMarkerImage(
            markerSize,
            markerOffset,
            normalOrigin
          ),
          overImage = this.createMarkerImage(
            overMarkerSize,
            overMarkerOffset,
            overOrigin
          ),
          clickImage = this.createMarkerImage(
            markerSize,
            markerOffset,
            clickOrigin
          );

        var position = new kakao.maps.LatLng(
          positions[i].latitude,
          positions[i].longitude
        );

        // 마커를 생성합니다
        const marker = new kakao.maps.Marker({
          map: map,
          position: position,
          title: positions[i].name,
          image: normalImage,
        });

        marker.normalImage = normalImage;
        marker.idx = i;

        // 마커에 표시할 인포윈도우를 생성합니다
        var infowindow = new kakao.maps.InfoWindow({
          content: `<div style="width:150px;text-align:center;padding:6px 0;">${positions[i].name}</div>`, // 인포윈도우에 표시할 내용
        });

        kakao.maps.event.addListener(
          marker,
          "mouseover",
          makeOverListener(map, marker, infowindow, overImage)
        );
        kakao.maps.event.addListener(
          marker,
          "mouseout",
          makeOutListener(map, marker, infowindow, normalImage)
        );
        kakao.maps.event.addListener(
          marker,
          "click",
          makeClickListener(map, marker, infowindow, clickImage)
        );

        //지도 범위에 추가
        bounds.extend(position);
        this.recommendMarkers.push(marker);
        // selectedMarker = self.clickCardChangeMarker(marker, normalImage,overImage,clickImage)
      }
      function makeOverListener(map, marker, infowindow, overImage) {
        return function() {
          infowindow.open(map, marker);
          if (!selectedMarker || selectedMarker !== marker) {
            marker.setImage(overImage);
          }
          self.actionMouseOverToCard(marker.idx);
        };
      }
      function makeOutListener(map, marker, infowindow, normalImage) {
        return function() {
          infowindow.close();
          //클릭된 마커가 없고, mouseout된 마커가 클릭된 마커가 아니면
          // 마커의 이미지를 기본 이미지로 변경합니다
          if (!selectedMarker || selectedMarker !== marker) {
            marker.setImage(normalImage);
          }
          self.actionMouseOverToCard(null);
        };
      }
      function makeClickListener(map, marker, infowindow, clickImage) {
        return function() {
          //클릭된 마커가 없고, click 마커가 클릭된 마커가 아니면
          // 마커의 이미지를 클릭 이미지로 변경합니다
          if (!selectedMarker || selectedMarker !== marker) {
            // 클릭된 마커 객체가 null이 아니면
            // 클릭된 마커의 이미지를 기본 이미지로 변경하고
            !!selectedMarker &&
              selectedMarker.setImage(selectedMarker.normalImage);

            // 현재 클릭된 마커의 이미지는 클릭 이미지로 변경합니다
            marker.setImage(clickImage);
            // }
          }
          // 클릭된 마커를 현재 클릭된 마커 객체로 설정합니다
          selectedMarker = marker;
          this.selectedMarker = selectedMarker;
          infowindow.close();
          window.$cookies.set("selectedMarker", selectedMarker.idx);
          self.actionClicked(selectedMarker.idx);
          // self.selectRest(selectedMarker.idx)
        };
      }

      // LatLngBounds 객체에 추가된 좌표들을 기준으로 지도의 범위를 재설정합니다
      // 이때 지도의 중심좌표와 레벨이 변경될 수 있습니다
      map.setBounds(bounds);
      this.showMarkers(this.recommendMarkers);
    },

    // MakrerImage 객체를 생성하여 반환하는 함수입니다
    createMarkerImage(markerSize, offset, spriteOrigin) {
      var SPRITE_MARKER_URL =
        "https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/markers_sprites2.png"; // 스프라이트 마커 이미지 URL
      var SPRITE_WIDTH = 126, // 스프라이트 이미지 너비
        SPRITE_HEIGHT = 146; // 스프라이트 이미지 높이
      var spriteImageSize = new kakao.maps.Size(SPRITE_WIDTH, SPRITE_HEIGHT); // 스프라이트 이미지의 크기

      var markerImage = new kakao.maps.MarkerImage(
        SPRITE_MARKER_URL, // 스프라이트 마커 이미지 URL
        markerSize, // 마커의 크기
        {
          offset: offset, // 마커 이미지에서의 기준 좌표
          spriteOrigin: spriteOrigin, // 스트라이프 이미지 중 사용할 영역의 좌상단 좌표
          spriteSize: spriteImageSize, // 스프라이트 이미지의 크기
        }
      );

      return markerImage;
    },
    createStarMarkerImage(markerSize, offset, spriteOrigin) {
      var SPRITE_MARKER_URL =
        "https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/markerStar.png"; // 스프라이트 마커 이미지 URL
      var SPRITE_WIDTH = 126, // 스프라이트 이미지 너비
        SPRITE_HEIGHT = 146; // 스프라이트 이미지 높이
      var spriteImageSize = new kakao.maps.Size(SPRITE_WIDTH, SPRITE_HEIGHT); // 스프라이트 이미지의 크기

      var markerImage = new kakao.maps.MarkerImage(
        SPRITE_MARKER_URL, // 스프라이트 마커 이미지 URL
        markerSize, // 마커의 크기
        {
          offset: offset, // 마커 이미지에서의 기준 좌표
          spriteOrigin: spriteOrigin, // 스트라이프 이미지 중 사용할 영역의 좌상단 좌표
          spriteSize: spriteImageSize, // 스프라이트 이미지의 크기
        }
      );

      return markerImage;
    },

    showPaths() {
      var plans = this.getPlanList;
      var map = this.map;
      var imageSrc =
        "https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/markerStar.png";
      plans.forEach((plan) => {
        var position = new kakao.maps.LatLng(plan.latitude, plan.longitude);
        plan.latlng = position;
      });
      if (this.curPath.length) {
        for (let i = 0; i < this.curPath.length; i++) {
          this.curPath[i].setMap(null);
        }
      }
      for (var i = 1; i < plans.length; i++) {
        var linePath = [plans[i - 1].latlng, plans[i].latlng];

        // 지도에 표시할 선을 생성합니다
        var polyline = new kakao.maps.Polyline({
          path: linePath, // 선을 구성하는 좌표배열 입니다
          strokeWeight: 5, // 선의 두께 입니다
          strokeColor: "#FFAE00", // 선의 색깔입니다
          strokeOpacity: 0.7, // 선의 불투명도 입니다 1에서 0 사이의 값이며 0에 가까울수록 투명합니다
          strokeStyle: "solid", // 선의 스타일입니다
        });

        // 지도에 선을 표시합니다
        this.curPath.push(polyline);
        polyline.setMap(map);
      }
      plans.forEach((plan) => {
        // 마커 이미지의 이미지 크기 입니다
        var imageSize = new kakao.maps.Size(24, 35);
        // 마커 이미지를 생성합니다
        var markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize);
        // 마커를 생성합니다
        var marker = new kakao.maps.Marker({
          map: map,
          position: plan.latlng,
          title: plan.title,
          image: markerImage,
        });
        var infowindow = new kakao.maps.InfoWindow({
          content: `<h5>${plan.name}</h5>`, // 인포윈도우에 표시할 내용
        });
        var OVER_MARKER_WIDTH = 27, // 오버 마커의 너비
          OVER_MARKER_HEIGHT = 42; // 오버 마커의 높이
        var overMarkerSize = new kakao.maps.Size(
          OVER_MARKER_WIDTH,
          OVER_MARKER_HEIGHT
        ); // 오버 마커의 크기
        const overImage = new kakao.maps.MarkerImage(imageSrc, overMarkerSize);

        kakao.maps.event.addListener(
          marker,
          "mouseover",
          makeOverListener(map, marker, infowindow, overImage)
        );
        kakao.maps.event.addListener(
          marker,
          "mouseout",
          makeOutListener(map, marker, infowindow, markerImage)
        );

        let selectedMarker = this.selectedMarker;
        // const self = this
        function makeOverListener(map, marker, infowindow, overImage) {
          return function() {
            infowindow.open(map, marker);
            if (!selectedMarker || selectedMarker !== marker) {
              marker.setImage(overImage);
            }
          };
        }
        function makeOutListener(map, marker, infowindow, normalImage) {
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
      });
    },
  },
};
</script>

<style scoped>
.map-top {
  position: absolute;
  z-index: 10;
  width: 100%;
  margin: auto;
}

#map {
  width: 100%;
  height: 500px;
  margin-left: auto;
  margin-right: auto;
}
</style>
