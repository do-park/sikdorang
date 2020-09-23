<template>
  <div class="d-flex flex-column">
      {{getSchedules}}
      <!-- <div v-for="schedule in schedules" :key="schedule.id">
          {{schedule}}
      </div> -->
  </div>
</template>

<script>
import { mapGetters } from "vuex"
export default {
    name : 'ScheduleProgress',
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