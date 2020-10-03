<template>
    <div class="row tour" @click="onClick">
        <div class="col-3 p-0">
            <img class="tour-title-img" :src="tour.title_img" alt="">
        </div>
        <div class="col-9 p-0 my-auto">
            <div class="tour-title text-truncate">[{{ tour.area}}]{{ tour.title }}</div>
            <div class="tour-date">{{ tour.start_date }}~{{ tour.end_date }}</div>
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
            this.$router.push(`/trip/detail/${this.tour.id}`)
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