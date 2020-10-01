<template>
    <div class="row m-0">
        <img :src="imgSrc" alt="" class="col-4 p-0 main-img">
        <div class="col-8 p-0">
            <h5 class="m-0">[{{ item.area }}]{{ item.title }}</h5>
            <div><small>{{ startDate }} ~ {{ endDate }}</small></div>
            <div>{{ item.price }} 원</div>
            <div v-if="finish"><small>인원 마감!</small></div>
            <div v-else class="row">
                <div class="col-3">{{ item.now_person }} / {{ item.limit_person }}</div>
                <div v-if="ready" class="col-9"><small>즉시 출발!</small></div>
                <div v-else class="col-9"><small>최소인원({{ item.departure_person }}) 달성 시 출발</small></div>
            </div>
        </div>
        
    </div>
</template>

<script>
export default {
    name: "TripProductItem",
    props: {
        item: Object,
    },
    data() {
        return {
            startDate: `${this.item.start_date.split('-')[0]}년 ${this.item.start_date.split('-')[1]}월 ${this.item.start_date.split('-')[2]}일`,
            endDate: `${this.item.end_date.split('-')[0]}년 ${this.item.end_date.split('-')[1]}월 ${this.item.end_date.split('-')[2]}일`,
            finish: this.item.limit_person === this.item.now_person,
            ready: this.item.now_person >= this.item.departure_person,
        }
    },
    computed: {
        imgSrc() {
            return this.$store.state.IMG_SERVER_URL + this.item.title_img
        }
    }
}
</script>

<style>

.main-img {
    object-fit: contain;
}

</style>