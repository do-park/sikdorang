<template>
    <div class="tour" @click="onClick">
        <div>{{ tour.title_img }}</div>
        <div>[{{ tour.area}}]{{ tour.title }}</div>
        <div>{{ tour.start_date }}~{{ tour.end_date }}</div>
        <div>{{ tour.price }}원</div>
    </div>
</template>

<script>

export default {
    name: "TripListItem",
    props: {
        tour: Object
    },
    methods: {
        onClick() {
            this.$router.push(`/trip/detail/${this.tour.id}`)
        }
    }
}
</script>

<style scoped>
.tour {
    cursor: pointer;
    border: 1px black solid;
}
</style>