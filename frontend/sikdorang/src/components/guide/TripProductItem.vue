<template>
    <div>
        <img :src="item.img" alt="">
        <h3>[{{ item.area }}]{{ item.title }}</h3>
        <div>{{ startDate }} ~ {{ endDate }}</div>
        <div>1인 : {{ item.price }} 원</div>
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
        }
    },
}
</script>

<style>

</style>