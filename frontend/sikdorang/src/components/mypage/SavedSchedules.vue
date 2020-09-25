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
       saveSchedule() {
           const scheduleData = []
           if (this.getSchedules.length > 0) {
               this.getSchedules.forEach(schedule => {
                   scheduleData.push({
                       //스케줄의 이름은 어디서 확인이 가능한가?????????
                       //스케줄 ERD는 있는건가?
                       //스케줄은 어디 저장되고 있나?
                       "schedule_idx" : schedule.idx,
                       "category_id" : schedule.id,
                       "category_name" : schedule.name,
                       "store_id" : schedule.userChoice.id,
                       "store_name" : schedule.userChoice.name,
                       "address" : schedule.userChoice.address,
                       "latitude" : schedule.userChoice.latitude,
                       "longtitude" : schedule.userChoice.longtitude,
                       "store_category" : schedule.userChoice.category,
                       "store_tags" : schedule.userChoice.tags
                   })
               });
           }

           console.log(scheduleData)
           const requestHeaders = {
                headers: {
                    Authorization: `JWT ${this.$cookies.get('auth-token')}`
                },
                scheduleData : scheduleData
            }
           this.$axios.post(`/saveschedule/`, requestHeaders )
            .then((res) => {
              console.log("일정을 저장했습니다.",res)
            })
            .catch((err) => {
              console.error(err);
            });
       },

       //오늘의 스케줄과 모든 스케줄을 받아온다
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

        // getTodaySchedules() {
        //     const requestHeaders = {
        //         headers: {
        //             Authorization: `JWT ${this.$cookies.get('auth-token')}`
        //         }
        //     }
        //     this.$axios.get('schedules',requestHeaders)
        //     .then(res=>{
        //         this.todaySchedule = res.data
        //     })
        //     .catch(err=>{
        //         console.log(err)
        //     })
        // },
        // getAllSchedules() {
        //     const requestHeaders = {
        //         headers: {
        //             Authorization: `JWT ${this.$cookies.get('auth-token')}`
        //         }
        //     }
        //     this.$axios.get('schedules',requestHeaders)
        //     .then(res=>{
        //         this.allSchedule = res.data
        //     })
        //     .catch(err=>{
        //         console.log(err)
        //     })
        // },
     
    },
}
</script>

<style>

</style>