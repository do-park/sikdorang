<template>
  <div v-if="tripList">
    <div v-if="todaySchedule.name">
      <div class="row name-date">
        <div class="col-8 p-0 schedule-name text-truncate">{{ todaySchedule.name }}</div>
        <div class="col-4 p-0 text-right schedule-date">{{ todaySchedule.date }}</div>
      </div>
      <MyPageMap :todaySchedule="todaySchedule.schedules"/>
      <TripListItem :todaySchedule="todaySchedule" :todayReviewList="todayReviewList"/>
    </div>
    <div v-else class="name-date">오늘 일정이 없습니다.</div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
import MyPageMap from "../mypage/MyPageMap.vue"
import TripListItem from "./TripListItem.vue"

const mypage = "mypage";

export default {
  name: "TripList",
  props: {
    tripList: Boolean,
  },
  components: {
    MyPageMap,
    TripListItem,
  },
  computed: {
    ...mapGetters("schedule", [
      "getSchedules",
      "getScheduleName",
      "getScheduleDate",
    ]),
    ...mapGetters(mypage, ["getTripList"]),
  },
  data() {
    return {
      todaySchedule: { id: "", name: "", date: "", schedules: [] },
      todayReviewList: [],
    };
  },
  created() {
    if (this.getSchedules.length === 0) {
      this.initiateSchedule();
    } else {
      this.saveSchedule();
    }
    this.getTodaySchedules();
  },
  mounted() {
  },
  methods: {
    ...mapActions("schedule", [
      "actionSchedule",
      "actionScheduleName",
      "actionScheduleDate",
    ]),
    popupPartyForm() {
      if (document.getElementById("partyForm").classList.contains("d-none")) {
        document.getElementById("partyForm").classList.remove("d-none");
        window.$cookies.set("party-trip-id", this.todaySchedule.id);
      } else {
        document.getElementById("partyForm").classList.add("d-none");
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
    async saveSchedule() {
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
      await this.$axios
        .post("/trip/", data, requestHeaders)
        .then(() => {
          this.initiateSchedule();
          location.reload()
          this.$router.go()
        })
        .catch((err) => {
          console.error(err);
        });
    },
    //오늘 일정 가져오기
    async getTodaySchedules() {
      const requestHeaders = {
        headers: {
          Authorization: `JWT ${this.$cookies.get("auth-token")}`,
        },
      };
      await this.$axios
        .get("/trip/today", requestHeaders)
        .then((res) => {
          this.makeScheduleList(res.data[0]);
          this.todayReviewList = res.data[1];
        })
        .catch((err) => {
          console.log(err);
        });
    },
    async restuarantPlan(i, id, type, typeName) {
      await this.$axios
        .get(`/trip/store_detail/${id}`)
        .then((res) => {
          const result = res.data;

          //가게의 타입도 구분
          if (type === "C") {
            typeName = "카페";
          }
          result["type"] = typeName;
          this.$set(this.todaySchedule.schedules, i, result);
          return result;
        })
        .catch((err) => {
          console.log(err);
          return [];
        });
    },
    async TourAPIPlan(i, id, type) {
      let contentTypeId = 32;
      let typeName = "숙박";
      if (type === "S") {
        contentTypeId = 12;
        typeName = "관광지";
      }
      const TOUR_API_KEY = this.$store.state.TOUR_API_KEY
      const contentId = id;
      await this.$axios
        .get(
          `http://api.visitkorea.or.kr/openapi/service/rest/KorService/detailCommon?ServiceKey=${TOUR_API_KEY}&contentId=${contentId}&contentTypeId=${contentTypeId}&MobileOS=ETC&MobileApp=TourAPI3.0_Guide&defaultYN=Y&firstImageYN=Y&areacodeYN=Y&catcodeYN=Y&addrinfoYN=Y&mapinfoYN=Y&overviewYN=Y&transGuideYN=Y`
        )
        .then((res) => {
          const items = res.data.response.body.items.item;
          // this.scheduleList["schedules"][String(i)] = {
          let address = null
					if (typeof(items.addr2) !== "undefined") {
						address = items.addr1 + items.addr2
					} else {
						address = items.addr1
					}
          let result = {
            id: items.contentid,
            store_name: items.title,
            branch: "",
            tel: items.tel,
            address: address,
            latitude: items.mapy,
            longitude: items.mapx,
            //category가 있지만, 식당/카페와 동일하게&혼선 안되게 하기 위해 type을 또 넣음.
            type: `${typeName}`,
            category: `${typeName}`,
            tags: "",
            img: items.firstimage,
          };
          this.$set(this.todaySchedule.schedules, i, result);
          return result;
        })
        .catch((err) => {
          console.error(err);
          return [];
        });
    },
    //일정 정보 가져오면 스케줄 리스트로 만들기
    async makeScheduleList(data) {
      this.todaySchedule.name = data.name;
      const stringDate = data.date.toString()
      this.todaySchedule.date = `${stringDate.substr(0,4)}-${stringDate.substr(4,2)}-${stringDate.substr(6,2)}`

      //일정 리스트로 만들기
      const plans = data.plan.split("-");
      this.todaySchedule.schedules = new Array(plans.length).fill(0);

      for (var i = 0; i < plans.length; i++) {
        let plan = plans[i];
        const type = plan.slice(0, 1);
        let typeName = "식당";
        const id = plan.slice(1);

        // 식당/카페이면
        if ((type === "R") | (type === "C")) {
          await this.restuarantPlan(i, id, type, typeName);
        }
        // 관광지/숙박이면
        else {
          await this.TourAPIPlan(i, id, type);
        }
      }
    },
  },
};
</script>

<style scoped>
.name-date {
  margin: 0px 5px;
}
.schedule-name {
  font-size: 20px;
  font-weight: bold;
}
.schedule-date {
  font-size: 16px;
  height: 18px;
  margin: auto;
}
.schedule-wrap {
  margin: 5px;
}
.schedule-detail {
  margin: 1rem 0px;
  padding: 0.5rem;
  background-color: whitesmoke;
  border-radius: 20px;
}
.detail-tel {
  font-size: 13px;
}
.detail-address {
  font-size: 12px;
}
.review-btn {
  font-size: 11px;
  background-color: crimson;
  color: white;
  padding: 2px;
  border-radius: 20%;
}
.review-finish {
  font-size: 11px;
  background-color: gray;
  color: white;
  padding: 2px;
  border-radius: 20%;
}
</style>
