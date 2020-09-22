<template>
    <div>
        <!-- 가이드를 검색하는 Input이 필요할 확률이 높음 -->
        <div class="item-wrap" v-for="item in tripProductList" :key="item.id" @click="goTripProductDetailPage(item.id)">
            <TripProductItem :item="item"/>
        </div>
    </div>
</template>

<script>
import TripProductItem from "./TripProductItem.vue"

export default {
    name: "TripProductList",
    components: {
        TripProductItem,
    },
    data() {
        return {
            index: 1,
            tripProductList: [
                {id: 1,
                user: 1,
                title_img: '이미지',
                title: '가을 여행',
                area: '구미',
                start_date: Date(2020-9-22),
                end_date: Date(2020-9-26),
                price: 50000,
                start_point: '인동 입석',
                start_time: '09:00'
                },
                {id: 2,
                user: 2,
                title_img: '이미지',
                title: '가을 여행',
                area: '구미',
                start_date: Date(2020,9,22),
                end_date: Date(2020,9,23),
                price: 50000,
                start_point: '인동 입석',
                start_time: '09:00'
                },
                {id: 3,
                user: 3,
                title_img: '이미지',
                title: '가을 여행',
                area: '구미',
                start_date: Date(2020,9,22),
                end_date: Date(2020,9,23),
                price: 50000,
                start_point: '인동 입석',
                start_time: '09:00'
                }
            ],
            targetGuide: null,
        }
    },
    mounted() {
        // this.$axios.get(`/trip/list/${this.index}`)
        // .then(res => {
        //     console.log(res)
        //     this.index += 1
        // })
        // .catch(err => console.error(err))
    },
    methods: {
        goTripProductDetailPage(item_pk) {
            this.$router.push(`/trip/detail/${item_pk}`)
        },
        getThatGuideList() {
            this.$axios.get(`/trip/list/${this.targetGuide}`)
            .then(res => {
                console.log(res)
                // this.tripProductList = res.data
            })
            .catch(err => console.log(err))
        },
    }
}
</script>

<style>
.item-wrap {
    cursor: pointer;
}

</style>