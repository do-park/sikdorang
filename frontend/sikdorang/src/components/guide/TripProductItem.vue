<template>
    <div>
        <img :src="item.img" alt="">
        <h3>[{{ item.area }}]{{ item.title }}</h3>
        <div>{{ item.start_date.substr(0,10) }} ~ {{item.end_date.substr(0,10) }}</div>
        <div>{{ item.price }} 원</div>
    </div>
</template>

<script>
export default {
    name: "TripProductItem",
    props: {
        item: Object,
    }
}
</script>

<style>

</style>