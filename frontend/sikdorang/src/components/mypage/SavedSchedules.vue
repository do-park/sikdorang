<template>
  <div v-if="savedSchedules">
    <h3>오늘의 일정</h3>
    <div v-if="todaySchedule.name">
      {{ todaySchedule.name }} | {{ todaySchedule.date }} |
      <button>동행구하기</button>
    </div>
    <div v-else>오늘 일정이 없습니다.</div>
    <hr />
    <div
      v-for="(schedule, index) in todaySchedule.schedules"
      :key="schedule.id"
    >
      {{ schedule.id }}
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
    <h3>저장된 여행 일정</h3>
    <hr />
    <div v-if="allSchedule">
      <div v-for="(schedule, index) in allSchedule" :key="schedule.id">
        {{ index + 1 }} | {{ schedule.name }} | {{ schedule.date }}
        <button @click="popupPartyForm(schedule.id)">동행구하기</button>
        <PartyForm :id="schedule.id" class="party-form d-none" />
      </div>
    </div>
    <div v-else>등록된 일정이 없습니다.</div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
// import Swal from "sweetalert2";
import PartyForm from "../mypage/PartyForm.vue"

export default {
  name: "SavedSchedules",
  props: {
    savedSchedules: Boolean,
  },
  components: {
      PartyForm,
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
      todaySchedule: { name: "", date: "", schedules: [] },
      todayReviewList: [],
      allSchedule: [],
    };
  },
  mounted() {
    if (this.getSchedules.length === 0) {
      this.initiateSchedule();
    } else {
      this.saveSchedule();
    }
    this.getTodaySchedules();
    this.getAllSchedules();
  },
  methods: {
    ...mapActions("schedule", [
      "actionSchedule",
      "actionScheduleName",
      "actionScheduleDate",
    ]),
    popupPartyForm(targetId) {
      if (document.getElementById(targetId).classList.contains('d-none')) {
        var forms = document.getElementsByClassName('party-form')
        console.log('this',forms)
        for (let form of forms) {
          if (!(form.classList.contains('d-none'))) {
            form.classList.add('d-none')
          }
        }
        document.getElementById(targetId).classList.remove('d-none')
      } else {
        document.getElementById(targetId).classList.add('d-none')
      }
  
    },
    initiateSchedule() {
      this.actionSchedule([]);
      this.actionScheduleName("");
      this.actionScheduleDate("");
    },
    
    goReviewForm(store_id) {
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
          this.makeScheduleList(res.data[0]);
          this.todayReviewList = res.data[1];
        })
        .catch((err) => {
          console.log(err);
        });
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
    //일정 정보 가져오면 스케줄 리스트로 만들기
    makeScheduleList(data) {
      this.todaySchedule.name = data.name;
      this.todaySchedule.date = data.date;

      //일정 리스트로 만들기
      const plans = data.plan.split("-");
      plans.forEach((plan) => {
        const type = plan.slice(0, 1);
        let typeName = "식당";
        const id = plan.slice(1);

        // 식당/카페이면
        if ((type === "R") | (type === "C")) {
          this.$axios
            .get(`trip/store_detail/${id}`)
            .then((res) => {
              const result = res.data;

              //가게의 타입도 구분
              if (type === "C") {
                typeName = "카페";
              }
              result["type"] = typeName;
              this.todaySchedule.schedules.push(result);
            })
            .catch((err) => {
              console.log(err);
            });
        }
        // 관광지/숙박이면
        else {
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

              this.todaySchedule.schedules.push({
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
              });

            })
            .catch((err) => console.error(err));
        }
      });
      console.log("오늘의 일정", this.todaySchedule);
    },
  },
};
</script>

<style>
</style>