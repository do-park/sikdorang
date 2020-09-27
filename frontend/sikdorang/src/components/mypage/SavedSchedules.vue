<template>
  <div>
      <h3>오늘의 일정</h3>
        {{todaySchedule.name}} | {{todaySchedule.date}} | <button>동행구하기</button> 
        <hr>
        <div
        v-for="schedule in todaySchedule.schedules"
        :key="schedule.id"
        >
             <div v-if="( schedule.type ==='식당' | schedule.type === '카페')">
                [{{schedule.type}}] {{schedule.store_name}} | <button>리뷰쓰기</button>
            </div>
            <div v-else>
                [{{schedule.type}}] {{schedule.name}}
            </div>

        </div>
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
            todaySchedule : {"name" : "", "date" : "", "schedules" : []},
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
        makeScheduleList(data) {
            console.log(data)
            this.todaySchedule.name = data.name
            this.todaySchedule.date = data.date

            //일정 리스트로 만들기
            const plans = data.plan.split('-')
            console.log(plans)
            plans.forEach(plan=>{
                const type = plan.slice(0,1)
                const typeName = "식당"
                const id = plan.slice(1,)

                // 식당/카페이면
                if (type === "R" | type === "C"  ) {
                    this.$axios.get(`trip/store_detail/${id}`)
                    .then(res=>{
                        const result = res.data

                        //가게의 타입도 구분
                        if (type === "C") { typeName = "카페" }
                        result["type"] = typeName 
                        this.todaySchedule.schedules.push(result)
                    })
                    .catch(err=>{
                        console.log(err)
                    })
                }
                // 관광지/숙박이면
                else {
                    const contentTypeId = 32
                    typeName ="숙박"
                    if (type === "S") { contentTypeId = 12; typeName = "관광지"; }
                    const TOUR_API_KEY = "K%2FplKHR5Hx7sLQwMexw4LCgDz45JjMDfJ1czEyCx83EBoZHJLUOKe%2B56J93QhZ41DlYmdRy3b1LIpwlSh%2FxYfQ%3D%3D"
                    const contentId = id
                    this.$axios.get(`http://api.visitkorea.or.kr/openapi/service/rest/KorService/detailCommon?ServiceKey=${TOUR_API_KEY}&contentId=${contentId}&contentTypeId=${contentTypeId}&MobileOS=ETC&MobileApp=TourAPI3.0_Guide&defaultYN=Y&firstImageYN=Y&areacodeYN=Y&catcodeYN=Y&addrinfoYN=Y&mapinfoYN=Y&overviewYN=Y&transGuideYN=Y`)
                    .then(res => {
                        const items = res.data.response.body.items.item
                        for (let i=0;i<items.length;i++) {
                            this.recommends.push({
                                "id": items[i].contentid,
                                "name": items[i].title,
                                "branch": "",
                                "tel": items[i].tel,
                                "address": items[i].addr1 + items[i].addr2,
                                "latitude": items[i].mapy,
                                "longtitude": items[i].mapx,
                                //category가 있지만, 식당/카페와 동일하게&혼선 안되게 하기 위해 type을 또 넣음.
                                "type" :`${typeName}`,
                                "category": `${typeName}`,
                                "tags": "",
                                "img": items[i].firstimage,
                    })
                }
                        console.log(items)
                    })
                    .catch(err => console.error(err))
                }
                
            })
            console.log("오늘의 일정",this.todaySchedule)
        },
    },
}
</script>

<style>

</style>