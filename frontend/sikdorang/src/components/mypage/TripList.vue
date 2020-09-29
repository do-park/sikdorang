<template>
    <div v-if="tripList">
        <div v-if="todaySchedule.name">
        <h3>{{ todaySchedule.name }}</h3> 
        <p> {{ todaySchedule.date }} </p>
        <button class="btn btn-success" @click="popupPartyForm">동행구하기</button>
        <button class="btn btn-primary" data-toggle="modal" data-target="#todayMessage">동행 신청자 보기</button>
        <PartyForm id="partyForm" class="d-none" /> 
        <div>여기 지도가 들어갑니다.</div>   
        <hr>
         <div
            v-for="(schedule, index) in todaySchedule.schedules"
            :key="schedule.id"
            >
            <div v-if="(schedule.type === '식당') | (schedule.type === '카페')">
                [{{ schedule.type }}] {{ schedule.store_name }} |
                <button
                v-if="todayReviewList[index] === 0"
                class="btn btn-primary"
                @click="goReviewForm(schedule.id)"
                >
                리뷰작성
                </button>
                <span v-else>이미 리뷰 작성했음</span>
            </div>
            <div v-else>[{{ schedule.type }}] {{ schedule.name }}</div>
            </div>  

      <hr />
    </div>
    <div v-else>오늘 일정이 없습니다.</div>
    <hr />
     <!-- Modal -->
      <div class="modal fade" id="todayMessage" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="exampleModalLabel">동행 신청 현황</h5>
              <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                <span aria-hidden="true">&times;</span>
              </button>
            </div>
            <div class="modal-body">
              <PartyRequests :partyPk=1 />
            </div>
          </div>
        </div>
      </div>
    </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex"
import PartyForm from "../mypage/PartyForm.vue"
import PartyRequests from "../mypage/PartyRequests.vue"

const mypage = "mypage"

export default {
    name: 'TripList',
    props : {
      tripList : Boolean,
    },
    components: {
      PartyForm,
      PartyRequests
    },
    computed: {
    ...mapGetters("schedule", [
      "getSchedules",
      "getScheduleName",
      "getScheduleDate",
    ]),
    ...mapGetters(mypage, [
      'getTripList'
    ])
  },
  data() {
    return {
      todaySchedule: { id: "", name: "", date: "", schedules: [] },
      todayReviewList: [],
     
    };
  },
  mounted() {
    if (this.getSchedules.length === 0) {
      this.initiateSchedule();
    } else {
      this.saveSchedule();
    }
    console.log(this.getScheduleName);
    console.log(this.getScheduleDate);
    this.getTodaySchedules();
   
  },
  methods: {
    ...mapActions("schedule", [
      "actionSchedule",
      "actionScheduleName",
      "actionScheduleDate",
    ]),
    popupPartyForm() {
      if (document.getElementById('partyForm').classList.contains('d-none')) {
        document.getElementById('partyForm').classList.remove('d-none')
        window.$cookies.set("party-trip-id", this.todaySchedule.id);
      } else {
        document.getElementById('partyForm').classList.add('d-none')
      }
  
    },
    initiateSchedule() {
      this.actionSchedule([]);
      this.actionScheduleName("");
      this.actionScheduleDate("");
    },
    goReviewForm(store_id) {
      console.log(store_id);
      this.$cookies.set("review-store-id", store_id);
      this.$router.push({ name: "ReviewForm" });
    },
    getSightseeing() {
      const TOUR_API_KEY =
        "K%2FplKHR5Hx7sLQwMexw4LCgDz45JjMDfJ1czEyCx83EBoZHJLUOKe%2B56J93QhZ41DlYmdRy3b1LIpwlSh%2FxYfQ%3D%3D";

      this.$axios
        .get(
          `http://api.visitkorea.or.kr/openapi/service/rest/KorService/detailCommon?ServiceKey=${TOUR_API_KEY}&contentId=126733&contentTypeId=12&MobileOS=ETC&MobileApp=TourAPI3.0_Guide&defaultYN=Y&firstImageYN=Y&areacodeYN=Y&catcodeYN=Y&addrinfoYN=Y&mapinfoYN=Y&overviewYN=Y&transGuideYN=Y`
        )
        .then((res) => {
          const items = res.data.response.body.items.item;
          console.log(items);
        })
        .catch((err) => console.error(err));
    },
    saveSchedule() {
      const scheduleData = [];
      console.log(this.getSchedules);
      if (this.getSchedules.length > 0) {
        this.getSchedules.forEach((schedule) => {
          scheduleData.push(schedule.id + String(schedule.userChoice.id));
        });
      } else {
        return;
      }
      const data = {
        plan: scheduleData.join("-"),
        name: this.getScheduleName,
        date: this.getScheduleDate,
      };
      const requestHeaders = {
        headers: {
          Authorization: `JWT ${this.$cookies.get("auth-token")}`,
        },
      };
      this.$axios
        .post("/trip/", data, requestHeaders)
        .then((res) => {
          console.log("일정을 저장했습니다.", res);
          this.initiateSchedule();
        //   console.log("지워졌나?", this.getSchedules);
        })
        .catch((err) => {
          console.error(err);
        });
    },
    //오늘 일정 가져오기
    getTodaySchedules() {
      const requestHeaders = {
        headers: {
          Authorization: `JWT ${this.$cookies.get("auth-token")}`,
        },
      };
      this.$axios
        .get("/trip/today", requestHeaders)
        .then((res) => {
          console.log(res);
          console.log("오늘의 일정은?",this.todaySchedule.schedules)
          this.makeScheduleList(res.data[0]);
          this.todayReviewList = res.data[1];
        })
        .catch((err) => {
          console.log(err);
        });
    },
      async restuarantPlan(i,id,type,typeName) {
          this.$axios
            .get(`trip/store_detail/${id}`)
            .then((res) => {
              const result = res.data;

              //가게의 타입도 구분
              if (type === "C") {
                typeName = "카페";
              }
              result["type"] = typeName;            
              this.$set(this.todaySchedule.schedules, i, result)        
              return result
            })
            .catch((err) => {
              console.log(err);
              return []
            });
        },
      async TourAPIPlan(i,id,type) {
        let contentTypeId = 32;
        let typeName = "숙박";
        if (type === "S") {
          contentTypeId = 12;
          typeName = "관광지";
        }
        const TOUR_API_KEY =
          "K%2FplKHR5Hx7sLQwMexw4LCgDz45JjMDfJ1czEyCx83EBoZHJLUOKe%2B56J93QhZ41DlYmdRy3b1LIpwlSh%2FxYfQ%3D%3D";
        const contentId = id;
        this.$axios
          .get(
            `http://api.visitkorea.or.kr/openapi/service/rest/KorService/detailCommon?ServiceKey=${TOUR_API_KEY}&contentId=${contentId}&contentTypeId=${contentTypeId}&MobileOS=ETC&MobileApp=TourAPI3.0_Guide&defaultYN=Y&firstImageYN=Y&areacodeYN=Y&catcodeYN=Y&addrinfoYN=Y&mapinfoYN=Y&overviewYN=Y&transGuideYN=Y`
          )
          .then((res) => {
            const items = res.data.response.body.items.item;

            // this.scheduleList["schedules"][String(i)] = {
            let result = {
              id: items.contentid,
              name: items.title,
              branch: "",
              tel: items.tel,
              address: items.addr1 + items.addr2,
              latitude: items.mapy,
              longtitude: items.mapx,
              //category가 있지만, 식당/카페와 동일하게&혼선 안되게 하기 위해 type을 또 넣음.
              type: `${typeName}`,
              category: `${typeName}`,
              tags: "",
              img: items.firstimage,
            }
            this.$set(this.todaySchedule.schedules, i, result)
            return result
          })
          .catch((err) =>{
            console.error(err);
            return []
          }) 
      },
     //일정 정보 가져오면 스케줄 리스트로 만들기
    async makeScheduleList(data) {
      this.todaySchedule.name = data.name;
      this.todaySchedule.date = data.date;
     
      //일정 리스트로 만들기
      const plans = data.plan.split("-");
      this.todaySchedule.schedules = new Array(plans.length).fill(0);
      console.log("!!!!!!!!!!",this.todaySchedule.schedules)
      for (var i = 0; i < plans.length; i ++) {
        let plan = plans[i]
        const type = plan.slice(0, 1);
        let typeName = "식당";
        const id = plan.slice(1);

        // 식당/카페이면
        if ((type === "R") | (type === "C")) {
          await this.restuarantPlan(i,id,type,typeName)
        }
        // 관광지/숙박이면
        else {
          await this.TourAPIPlan(i,id,type)

        }
      }
    },
   
  },
};
</script>

<style>
</style>
