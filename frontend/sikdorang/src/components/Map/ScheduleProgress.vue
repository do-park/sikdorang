<template>
  <div class="d-flex flex-row justify-content-center">
      <div v-for="(schedule, index) in schedules" :key="schedule.idx">
          <schedule-progress-item class="m-2" :schedule="schedule" :index="index"/>
      </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex"
import ScheduleProgressItem from "./ScheduleProgressItem.vue"

export default {
    name : 'ScheduleProgress',
    components: {
        ScheduleProgressItem,
    },
    data() {
        return {
            schedules : [],
        }
    },
    mounted() {
        this.schedules = this.getSchedules
    },
    computed : {
        ...mapGetters("schedule",[
            'getSchedules',
        ])
    },
    methods : {

    },

}
</script>

<style>

</style>