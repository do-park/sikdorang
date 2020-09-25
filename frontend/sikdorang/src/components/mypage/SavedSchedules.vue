<template>
  <div>
      <h3>저장된 여행 일정</h3>
      <div class="d-flex">
          <div
          v-for="schedule in getSchedules"
          :key="schedule.index"
          >
            {{schedule.userChoice.name}} -->
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