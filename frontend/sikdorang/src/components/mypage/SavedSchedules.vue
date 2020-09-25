<template>
  <div>
      <h3>오늘의 일정</h3>

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
    data() {
        return {
            todaySchedule : [],
            allSchedule : [],
        }
    },
    methods : {
       
       //오늘의 스케줄과 모든 스케줄을 받아온다.
        getTodayAndAllSchedules() {
            const requestHeaders = {
                headers: {
                    Authorization: `JWT ${this.$cookies.get('auth-token')}`
                }
            }
            this.$axios.get('schedules',requestHeaders)
            .then(res=>{
                this.todaySchedule = res.data[0]
                this.allSchedule = res.data[1]
            })
            .catch(err=>{
                console.log(err)
            })
        },

        getTodaySchedules() {
            const requestHeaders = {
                headers: {
                    Authorization: `JWT ${this.$cookies.get('auth-token')}`
                }
            }
            this.$axios.get('schedules',requestHeaders)
            .then(res=>{
                this.todaySchedule = res.data
            })
            .catch(err=>{
                console.log(err)
            })
        },
        getAllSchedules() {
            const requestHeaders = {
                headers: {
                    Authorization: `JWT ${this.$cookies.get('auth-token')}`
                }
            }
            this.$axios.get('schedules',requestHeaders)
            .then(res=>{
                this.allSchedule = res.data
            })
            .catch(err=>{
                console.log(err)
            })
        },
     
    },
}
</script>

<style>

</style>