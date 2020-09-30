<template>
    <div>
        <div>식도랑 추천 코스 생성중</div>
    </div>
</template>

<script>
import { mapGetters } from 'vuex'
import axios from 'axios'

const CATEGORY_NAME = ["한식", "분식", "피자", "치킨", "돈가스/회/일식", "카페/디저트/베이커리", "아시안", "양식", "중식", "도시락", "패스트푸드","술집", "족발/보쌈", "찜/탕"]

export default {
    name: "SikdorangRecommendView",
    computed: {
        ...mapGetters('sikRec', ['getForUser']),
        ...mapGetters('schedule', ['getSchedules']),
    },
    data() {
        return {
            schedules: [],
            beforeLat: null,
            beforeLng: null,
            beforeCat: [],
        }
    },
    methods: {
        divideRecommendation(cf, index) {
			if (cf === "식당" | cf === "카페"){
				this.getSCRecommendation(cf, index)
			} else {
				this.getSHRecommendation(cf, index)
			}
		},
		async getSCRecommendation(cf, index) {
			const requestHeaders = {
				headers: {
					Authorization: `JWT ${this.$cookies.get('auth-token')}`
				}
            }
			await this.$axios.post('recommend/tag-recommend/', { category: cf, lat: this.beforeLat, lng: this.beforeLng, bc: this.beforeCat }, requestHeaders)
			.then(res => {
                const result = res.data.result[0]
                this.schedules[index].userChoice = result
                this.beforeLat = result.latitude
                this.beforeLng = result.longitude
                this.beforeCat.push(result.category)
			})
			.catch(err => console.error("알고리즘 추천 실패",err))
		},
		async getSHRecommendation(cf, index) {
			const TOUR_API_KEY = "K%2FplKHR5Hx7sLQwMexw4LCgDz45JjMDfJ1czEyCx83EBoZHJLUOKe%2B56J93QhZ41DlYmdRy3b1LIpwlSh%2FxYfQ%3D%3D"
            let contentTypeId = 32
            if (cf ==="관광지") { contentTypeId = 12 }
            await axios.get(`http://api.visitkorea.or.kr/openapi/service/rest/KorService/locationBasedList?ServiceKey=${TOUR_API_KEY}&contentTypeId=${contentTypeId}&mapX=${this.beforeLng}&mapY=${this.beforeLat}&radius=5000&listYN=Y&MobileOS=ETC&MobileApp=TourAPI3.0_Guide&arrange=A&numOfRows=12&pageNo=1&_type=json`)
            .then(res => {
                const items = res.data.response.body.items.item
                this.schedules[index].userChoice = {
                    "id": items[0].contentid,
                    "name": items[0].title,
                    "branch": "",
                    "tel": items[0].tel,
                    "address": items[0].addr1 + items[0].addr2,
                    "latitude": items[0].mapy,
                    "longitude": items[0].mapx,
                    "category": "관광지",
                    "tags": "",
                    "img": items[0].firstimage,
                }
                this.beforeLat = this.schedules[index].userChoice.latitude
                this.beforeLng = this.schedules[index].userChoice.longitude
                this.beforeCat.push(this.schedules[index].userChoice.category)
            })
            .catch(err => console.error(err))
		},
    },
    async mounted() {
        this.schedules = this.getSchedules
        this.beforeLat = this.getForUser.latitude
        this.beforeLng = this.getForUser.longitude
        for (let i=0; i<this.schedules.length; i++) {
            if (i == 0) {
                const forUser = this.getForUser
                this.schedules[i].userChoice = {
                    "id": forUser.id,
                    "name": forUser.store_name,
                    "branch": forUser.branch,
                    "tel": forUser.tel,
                    "address": forUser.address,
                    "latitude": forUser.latitude,
                    "longitude": forUser.longitude,
                    "category": CATEGORY_NAME[forUser.category],
                    "tags": forUser.tags,
                }
            } else {
                await this.divideRecommendation(this.schedules[i].name, i)
            }
        }
        console.log('추천 결과 확인', this.schedules)
        this.schedules.forEach(e => {
            console.log(e.userChoice)
        })
        // 생성 완료
    }
}
</script>

<style>

</style>