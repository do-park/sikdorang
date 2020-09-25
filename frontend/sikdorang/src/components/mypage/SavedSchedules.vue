<template>
  <div>
      <h3>저장된 여행 일정</h3>
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
}
</script>

<style>

</style>