<template>
  <div>
    <h3>저장된 여행 일정</h3>
    <div>
      <button class="btn btn-primary" @click="goReviewForm">리뷰작성 테스트</button>
    </div>
    <div>
      <div
      v-for="(schedule, index) in getSchedules"
      :key="schedule.idx"
      >
        {{index+1}}.{{schedule.userChoice.name}}
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex"

export default {
    name : "SavedSchedules",
    computed : {
        ...mapGetters("schedule",[
            "getSchedules"
        ])
    },
    methods: {
      goReviewForm() {
        this.$router.push({ name: "ReviewForm" });
      }
    },
}
</script>

<style>

</style>