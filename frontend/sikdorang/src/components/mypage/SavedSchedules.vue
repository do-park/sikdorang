<template>
  <div v-if="savedSchedules">
    <hr />
     <b-modal id="modal-scrollable" scrollable title="Scrollable Content">
       <h1>썸띵 지도 들어갈 곳</h1>
          <div class="my-4" v-for="(ListItem, index) in scheduleList" :key="ListItem.id">
              <div v-if="ListItem.type === '식당' | ListItem.type === '카페'">
                <p>
                 {{ index + 1 }} | [{{ListItem.type}}] {{ListItem.store_name}} | {{ListItem.address}}
                </p>
              </div>
              <div v-else>
                <p>
                {{ index + 1 }} | [ {{ListItem.type}} ] {{ListItem.name}} | {{ListItem.address}}

                </p>
              </div>
          </div>
    </b-modal>
    <div v-if="allSchedule">
      <div
        @click="goScheduleDetail(schedule)"
        v-for="(schedule, index) in allSchedule"
        :key="schedule.idx"
      >
        {{ index + 1 }} | {{ schedule.name }} | {{ schedule.date }} |
        <b-button v-b-modal.modal-scrollable>상세보기</b-button> |
        <button class="btn btn-success" @click="popupPartyForm(schedule.id)">
          동행구하기
        </button>
        <button class="btn btn-primary" data-toggle="modal" data-target="#targetMessage">동행 신청자 보기</button>
        <PartyForm :id="schedule.id" class="party-form d-none" />
        <hr />
        <!-- Modal -->
        <div class="modal fade" id="targetMessage" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
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
    </div>
    <div v-else>등록된 일정이 없습니다.</div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";

import PartyForm from "../mypage/PartyForm.vue";
import PartyRequests from "../mypage/PartyRequests.vue";

export default {
  name: "SavedSchedules",
  props: {
    savedSchedules: Boolean,
  },
  components: {
    PartyForm,
    PartyRequests,
  },
  computed: {
    ...mapGetters("schedule", [
      "getSchedules",
      "getScheduleName",
      "getScheduleDate",
    ]),
  },
  data() {
    return {
      allSchedule: [],
      scheduleList :[],
      scheduleName : '',
      scheduleDate : '',
    };
  },
  mounted() {
    this.getAllSchedules();
    this.today = new Date();
  },
  methods: {
    popupPartyForm(targetId) {
      if (document.getElementById(targetId).classList.contains("d-none")) {
        var forms = document.getElementsByClassName("party-form");
        // console.log("this", forms);
        for (let form of forms) {
          if (!form.classList.contains("d-none")) {
            form.classList.add("d-none");
          }
        }
        document.getElementById(targetId).classList.remove("d-none");
        window.$cookies.set("party-trip-id", targetId);
      } else {
        document.getElementById(targetId).classList.add("d-none");
      }
    },
    goScheduleDetail(schedule) {
      this.resetScheduleList()
      console.log(schedule.name)
      this.makeScheduleList(schedule)
      
    },
    resetScheduleList() {
      this.scheduleList = [],
      this.scheduleName = '',
      this.scheduleDate = ''
    },
    //모든 일정 가져오기
    getAllSchedules() {
      const requestHeaders = {
        headers: {
          Authorization: `JWT ${this.$cookies.get("auth-token")}`,
        },
      };
      this.$axios
        .get("/trip/list", requestHeaders)
        .then((res) => {
          this.allSchedule = res.data;
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
              this.$set(this.scheduleList, i, result)        
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
            this.$set(this.scheduleList, i, result)
            return result
          })
          .catch((err) =>{
            console.error(err);
            return []
          }) 
      },
        
    //일정 정보 가져오면 스케줄 리스트로 만들기
    async makeScheduleList(data) {
      this.scheduleName = data.name;
      this.scheduleDate = data.date;
     
      //일정 리스트로 만들기
      const plans = data.plan.split("-");
      this.scheduleList = new Array(plans.length).fill(0);
  
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
    stringtodate(str) {
      const y = str.substr(0, 4);
      const m = str.substr(5, 2);
      const d = str.substr(8, 2);
      return new Date(y, m - 1, d);
    },
  },
};
</script>

<style>
</style>