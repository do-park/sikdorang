<template>
    <div>
        <img :src="item.img" alt="">
        <h3>{{ item.title }}</h3>
        <span>{{ item.start_date }} ~ {{item.end_date }}</span>
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