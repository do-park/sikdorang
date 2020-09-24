<template>
    <div>
        <button @click="divideRecommendation('식당')">식당추천</button><br>
        <button @click="divideRecommendation('카페')">카페추천</button><br>
        <button @click="divideRecommendation('관광')">관광추천</button><br>
        <button @click="divideRecommendation('숙소')">숙소추천</button>
    </div>
</template>

<script>
import axios from "axios"


export default {
    name: "restest",
    data() {
        return {
            beforeLng: null,
			beforeLat: null,
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
			const requestHeaders = {
				headers: {
					Authorization: `JWT ${this.$cookies.get('auth-token')}`
				}
			}
			this.$axios.post('recommend/tag-based-rec/', {category: cf}, requestHeaders)
			.then(res => {
				console.log(res)
				// this.recommends = res.data
			})
			.catch(err => console.error(err))
		},
		getSHRecommendation(cf) {
			console.log('관광지 / 숙박 정보를 받습니다.', cf)
			const TOUR_API_KEY = "K%2FplKHR5Hx7sLQwMexw4LCgDz45JjMDfJ1czEyCx83EBoZHJLUOKe%2B56J93QhZ41DlYmdRy3b1LIpwlSh%2FxYfQ%3D%3D"
			axios.get(`http://api.visitkorea.or.kr/openapi/service/rest/KorService/locationBasedList?ServiceKey=${TOUR_API_KEY}&contentTypeId=&mapX=${this.beforeLng}&mapY=${this.beforeLat}&radius=2000&listYN=Y&MobileOS=ETC&MobileApp=TourAPI3.0_Guide&arrange=A&numOfRows=12&pageNo=1&_type=json`)
			.then(res => {
				console.log(res)
			})
			.catch(err => console.error(err))
		},
    },
}
</script>

<style>

</style>