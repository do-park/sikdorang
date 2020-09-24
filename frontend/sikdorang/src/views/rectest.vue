<template>
    <div>
        <button @click="divideRecommendation('식당')">식당추천</button>
        <br>
        <button @click="divideRecommendation('카페')">카페추천</button>
        <br>
        <button @click="divideRecommendation('관광지')">관광지추천</button>
        <br>
        <button @click="divideRecommendation('숙박')">숙박추천</button>
        <hr>
        <div v-for="recommend in recommends" :key="recommend.id">
            <img v-if="recommend.img" :src="recommend.img" alt="">
            <p>{{ recommend.id }}</p>
            <p>{{ recommend.name }}</p>
            <p>{{ recommend.tel }}</p>
            <p>{{ recommend.address }}</p>
            <p>{{ recommend.latitude }}</p>
            <p>{{ recommend.longtitude }}</p>
            <p>{{ recommend.category }}</p>
            <p>{{ recommend.tags }}</p>
            <hr>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: "RECTEST",
    data() {
        return {
            beforeLng: 128.4128223,
            beforeLat: 36.109328,
            recommends: [],
        }
    },
    methods: {
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
				console.log(res)
				this.recommends = res.data.result
			})
			.catch(err => console.error(err))
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
                console.log(items)
            })
            .catch(err => console.error(err))
		},
    }
}
</script>

<style>

</style>