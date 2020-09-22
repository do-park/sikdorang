<template>
    <div>
        <img :src="item.img" alt="">
        <h3>{{ item.title }}</h3>
        <span>{{ item.start_date.substr(0,10) }} ~ {{item.end_date.substr(0,10) }}</span>
        <span>{{ item.price }} 원</span>
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