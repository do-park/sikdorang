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
            "getSchedules",
            "getScheduleName",
            "getScheduleDate"
        ])
    },
    data() {
        return {
            todaySchedule : [],
            allSchedule : [],
        }
    },
    mounted() {
        this.saveSchedule()
        console.log(this.getScheduleName)
        console.log(this.getScheduleDate)
        this.getTodaySchedules()
        this.getAllSchedules()
    },
    methods : {
       getSightseeing() {
           const TOUR_API_KEY = "K%2FplKHR5Hx7sLQwMexw4LCgDz45JjMDfJ1czEyCx83EBoZHJLUOKe%2B56J93QhZ41DlYmdRy3b1LIpwlSh%2FxYfQ%3D%3D"
           
            this.$axios.get(`http://api.visitkorea.or.kr/openapi/service/rest/KorService/detailCommon?ServiceKey=${TOUR_API_KEY}&contentId=126733&contentTypeId=12&MobileOS=ETC&MobileApp=TourAPI3.0_Guide&defaultYN=Y&firstImageYN=Y&areacodeYN=Y&catcodeYN=Y&addrinfoYN=Y&mapinfoYN=Y&overviewYN=Y&transGuideYN=Y`)
            .then(res => {
                const items = res.data.response.body.items.item
                console.log(items)
            })
            .catch(err => console.error(err))
       },
       saveSchedule() {
           const scheduleData = []
           if (this.getSchedules.length > 0) {
               this.getSchedules.forEach(schedule => {
                   scheduleData.push(schedule.id+String(schedule.userChoice.id))
               });
           }
           const data = {
               "plan" :scheduleData.join('-'),
               "name" : this.getScheduleName,
               "date" : this.getScheduleDate
           }
           const requestHeaders = {
                headers: {
                    Authorization: `JWT ${this.$cookies.get('auth-token')}`,
                },

            }
           this.$axios.post('/trip/', data , requestHeaders)
            .then((res) => {
              console.log("일정을 저장했습니다.",res)
            })
            .catch((err) => {
              console.error(err);
            });
       },
        //오늘 일정 가져오기
        getTodaySchedules() {
            const requestHeaders = {
                headers: {
                    Authorization: `JWT ${this.$cookies.get('auth-token')}`
                }
            }
            this.$axios.get('/trip/today',requestHeaders)
            .then(res=>{
                console.log(res)
                this.makeScheduleList(res.data)
            })
            .catch(err=>{
                console.log(err)
            })
        },
        //모든 일정 가져오기
        getAllSchedules() {
            const requestHeaders = {
                headers: {
                    Authorization: `JWT ${this.$cookies.get('auth-token')}`
                }
            }
            this.$axios.get('/trip/list',requestHeaders)
            .then(res=>{
                console.log(res)
                // this.allSchedule = res.data
            })
            .catch(err=>{
                console.log(err)
            })
        },
        //일정 정보 가져오면 스케줄 리스트로 만들기
        makeScheduleList(info) {
            console.log(info)
            
        },
    },
}
</script>

<style>

</style>