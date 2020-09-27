<template>
    <div>
        <img :src="item.img" alt="">
        <h3>[{{ item.area }}]{{ item.title }}</h3>
        <div>{{ startDate }} ~ {{ endDate }}</div>
        <div>1인 : {{ item.price }} 원</div>
        <div v-if="finish">인원 마감!</div>
        <div v-else>
            <div>{{ item.now_person }} / {{ item.limit_person }}</div>
            <div v-if="ready">즉시 출발!</div>
            <div v-else>최소인원({{ item.departure_person }}) 달성 시 출발</div>
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
}
</script>

<style>

</style>