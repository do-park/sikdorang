<template>
  <div class="schedule-wrap">
        <div
            v-for="(schedule, index) in todaySchedule.schedules"
            :key="index"
        >
            <div class="row schedule-detail my-0">

                <div class="col-10 p-0 row m-0">
                    <div class="col-1 p-0">
                        <i v-if="(schedule.type === '식당')" class="fas fa-utensils" style="color: tomato"></i>
                        <i v-else-if="(schedule.type === '카페')" class="fas fa-coffee" style="color: sienna"></i>
                        <i v-else-if="(schedule.type === '관광지')" class="fas fa-place-of-worship" style="color: steelblue"></i>
                        <i v-else class="fas fa-bed" style="color: seagreen"></i>
                    </div>
                    <div class="col-6 p-0 font-weight-bold">
                        <div v-if="(schedule.type === '식당') | (schedule.type === '카페')" class="text-truncate">{{ schedule.store_name }}</div>
                        <div v-else class="text-truncate">{{ schedule.store_name }}</div>
                    </div>
                    <div class="col-5 p-0 detail-tel text-center">{{schedule.tel}}</div>
                    <div class="col-12 p-0 detail-address">{{schedule.address}}</div>
                </div>
                <div class="col-2 p-0 text-center" v-if="(schedule.type === '식당') | (schedule.type === '카페')">
                    <button
                    v-if="todayReviewList[index] === 0"
                    class="review-btn"
                    @click="goReviewForm(schedule.id)"
                    >
                    <i class="fas fa-keyboard fa-2x"></i>
                    <div>리뷰작성</div>
                    </button>
                    <button class="review-finish" v-else>
                    <i class="fas fa-keyboard fa-2x"></i>
                    <div>작성완료</div>
                    </button>
                </div>
            </div>
            <div v-if="todaySchedule.schedules.length-1 > index" class="my-3 text-center">
                <i class="fas fa-arrow-down ml-1"/><span class="small">{{ getTimeCheck[index].distance }}</span>
                <span class="my-0" style="background-color: #FFAE0055;">
                    <i class="fas fa-walking ml-1"/><span class="small">{{ getTimeCheck[index].walkMin }}</span>
                    <i class="fas fa-bicycle ml-1"/><span class="small">{{ getTimeCheck[index].bycicleMin }}</span>
                    <i class="fas fa-car ml-1"/><span class="small">{{ getTimeCheck[index].carMin }}</span>
                </span>
            </div>
        </div>
    </div>
</template>

<script>
import { mapGetters } from "vuex";

export default {
    name: "TripListItem",
    props: {
        todaySchedule: Object,
        todayReviewList: Array
    },
    computed: {
        ...mapGetters("mapEvent", ["getTimeCheck"]),
    }
}
</script>

<style scoped>
.name-date {
  margin: 0px 5px;
}
.schedule-name {
  font-size: 20px;
  font-weight: bold;
}
.schedule-date {
  font-size: 16px;
  height: 18px;
  margin: auto;
}
.schedule-wrap {
  margin: 5px;
}
.schedule-detail {
  margin: 1rem 0px;
  padding: 0.5rem;
  background-color: whitesmoke;
  border-radius: 20px;
}
.detail-tel {
  font-size: 13px;
}
.detail-address {
  font-size: 12px;
}
.review-btn {
  font-size: 11px;
  background-color: crimson;
  color: white;
  padding: 2px;
  border-radius: 20%;
}
.review-finish {
  font-size: 11px;
  background-color: gray;
  color: white;
  padding: 2px;
  border-radius: 20%;
}
</style>