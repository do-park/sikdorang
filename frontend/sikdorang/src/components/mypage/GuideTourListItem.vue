<template>
    <div class="row tour" @click="onClick">
        <div class="col-3 p-0">
            <img class="tour-title-img" :src="tour.trip_item.title_img" alt="">
        </div>
        <div class="col-9 p-0 my-auto">
            <div class="tour-title text-truncate">[{{ tour.trip_item.area}}]{{ tour.trip_item.title }}</div>
            <div class="tour-date">{{ tour.trip_item.start_date }}~{{ tour.trip_item.end_date }}</div>
        </div>
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
            this.$router.push(`/trip/detail/${this.tour.trip_item.id}`)
        }
    }
}
</script>

<style scoped>
.tour {
    cursor: pointer;
    margin: 1rem 5px;
}
.tour-title-img {
  display: block;
  width: 4rem;
  height: 4rem;
  border-radius: 50%;

  background-repeat: no-repeat;
  background-position: center center;
  background-size: cover;
} 
.tour-title {
    font-size: 15px;
    font-weight: bolder;
}
.tour-date {
    font-size: 13px;
}
</style>