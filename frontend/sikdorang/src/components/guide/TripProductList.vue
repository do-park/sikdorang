<template>
    <div>
        <!-- 가이드를 검색하는 Input이 필요할 확률이 높음 -->
        <div v-for="item in tripProductList" :key="item.id">
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
            tripProductList: [],
            targetGuide: null,
        }
    },
    mounted() {
        this.$axios.get(`/trip/list/${this.index}`)
        .then(res => {
            console.log(res)
            this.index += 1
        })
        .catch(err => console.error(err))
    },
    methods: {
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

</style>