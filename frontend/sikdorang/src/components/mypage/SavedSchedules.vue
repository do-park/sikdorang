<template>
  <div v-if="savedSchedules">
    <b-modal id="modal-scrollable" scrollable :title="scheduleName" hide-footer>
      <MyPageMap :todaySchedule="scheduleList"/>
      <div
        class="my-4"
        v-for="ListItem in scheduleList"
        :key="ListItem.id"
      >
        <div class="row m-0">
          <div class="col-1 p-0">
            <i v-if="ListItem.type === '식당'" class="fas fa-utensils"></i>
            <i v-else-if="ListItem.type === '카페'" class="fas fa-coffee"></i>
            <i
              v-else-if="ListItem.type === '관광지'"
              class="fas fa-place-of-worship"
            ></i>
            <i v-else class="fas fa-bed"></i>
          </div>
          <div class="col-6 p-0 font-weight-bold">
            <div
              v-if="(ListItem.type === '식당') | (ListItem.type === '카페')"
              class="text-truncate"
            >
              {{ ListItem.store_name }}
            </div>
            <div v-else class="text-truncate">{{ ListItem.store_name }}</div>
          </div>
          <div class="col-5 p-0 detail-tel text-center">{{ ListItem.tel }}</div>
          <div class="col-12 p-0 detail-address">{{ ListItem.address }}</div>
        </div>
      </div>
    </b-modal>
    <div v-if="allSchedule.length > 0" class="small-margin">
      <div
        @click="goScheduleDetail(schedule)"
        v-for="schedule in allSchedule"
        :key="schedule.idx"
        class="row m-0 mb-2"
      >
        <div class="col-8 p-0">
          <div v-b-modal.modal-scrollable class="schedule-name text-truncate">
            {{ schedule.name }}
          </div>
          <div>{{ schedule.date }}</div>
        </div>
        <div class="col-4 p-0 row m-0">
          <div class="col-6 p-0 text-center">
            <!-- 동행 상세페이지로 이동 -->
            <button
              v-if="schedule.party_chk"
              class=""
              @click="readParty(schedule.id)"
            >
              <i class="fas fa-users fa-2x icon-active"></i>
            </button>

            <!-- 동행 구하는 글 쓰기 -->
            <button
              v-else
              class=""
              @click="createParty(schedule.id, schedule.date)"
            >
              <i class="fas fa-users fa-2x icon-no-active"></i>
            </button>
          </div>
          <div class="col-6 p-0 text-center">
            <!-- 동행 활성화일 때 -->
            <PartyRequests v-if="schedule.party_chk" :partyPk="schedule.id" />

            <!-- 동행 비활성화일 때 -->
            <button v-else class="">
              <i class="fas fa-comment fa-2x icon-no-active"></i>
            </button>
          </div>
        </div>
      </div>
    </div>
    <div v-else class="small-margin">등록된 일정이 없습니다.</div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import PartyRequests from "../mypage/PartyRequests.vue";
import MyPageMap from "./MyPageMap.vue"

export default {
  name: "SavedSchedules",
  props: {
    savedSchedules: Boolean,
  },
  components: {
    MyPageMap,
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
      scheduleList: [],
      scheduleName: "",
      scheduleDate: "",
    };
  },
  async created() {
    await this.getAllSchedules();
    this.today = new Date();
  },
  methods: {
    getTripdata(tripId) {
      this.$axios
        .get(`/trip/${tripId}`)
        .then((res) => {
          this.$cookies.set("trip", res.data);
        })
        .catch((err) => {
          console.error(err);
        });
    },
    getPartydata(partyId) {
      this.$axios
        .get(`/party/detail_party/${partyId}`)
        .then((res) => {
          this.$cookies.set("party", res.data[0]);
        })
        .catch((err) => {
          console.error(err);
        });
    },
    readParty(scheduleId) {
      this.getPartydata(scheduleId);
      this.getTripdata(scheduleId);
      this.$router.push({ name: "PartyListItemDetail" });
    },
    createParty(scheduleId, scheduleDate) {
      this.$cookies.set("party-trip-id", scheduleId);
      var intDate = scheduleDate.split("-").join("") * 1;
      this.$cookies.set("party-trip-date", intDate);
      this.$cookies.set("party-type", 0);
      this.$router.push({ name: "PartyForm" });
    },
    popupPartyForm(targetId, targetDate) {
      if (document.getElementById(targetId).classList.contains("d-none")) {
        var forms = document.getElementsByClassName("party-form");
        for (let form of forms) {
          if (!form.classList.contains("d-none")) {
            form.classList.add("d-none");
          }
        }
        document.getElementById(targetId).classList.remove("d-none");
        window.$cookies.set("party-trip-id", targetId);
        window.$cookies.set("party-trip-date", targetDate);
      } else {
        document.getElementById(targetId).classList.add("d-none");
      }
    },
    async goScheduleDetail(schedule) {
      this.resetScheduleList();
      // this.makeScheduleList(schedule)
      await this.makeScheduleList(schedule);
    },
    resetScheduleList() {
      (this.scheduleList = []),
        (this.scheduleName = ""),
        (this.scheduleDate = "");
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
          res.data.forEach(function (target, index) {
            const stringDate = target.date.toString();
            res.data[index].date = `${stringDate.substr(
              0,
              4
            )}-${stringDate.substr(4, 2)}-${stringDate.substr(6, 2)}`;
          });
          this.allSchedule = res.data;
        })
        .catch((err) => {
          console.log(err);
        });
    },

    async restuarantPlan(i, id, type, typeName) {
      this.$axios
        .get(`trip/store_detail/${id}`)
        .then((res) => {
          const result = res.data;

          //가게의 타입도 구분
          if (type === "C") {
            typeName = "카페";
          }
          result["type"] = typeName;
          this.$set(this.scheduleList, i, result);
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
            store_name: items.title,
            branch: "",
            tel: items.tel,
            address: items.addr1 + items.addr2,
            latitude: items.mapy,
            longitude: items.mapx,
            //category가 있지만, 식당/카페와 동일하게&혼선 안되게 하기 위해 type을 또 넣음.
            type: `${typeName}`,
            category: `${typeName}`,
            tags: "",
            img: items.firstimage,
          };
          this.$set(this.scheduleList, i, result);
          return result;
        })
        .catch((err) => {
          console.error(err);
          return [];
        });
    },

    //일정 정보 가져오면 스케줄 리스트로 만들기
    async makeScheduleList(data) {
      this.scheduleName = data.name;
      this.scheduleDate = data.date;

      //일정 리스트로 만들기
      const plans = data.plan.split("-");
      this.scheduleList = new Array(plans.length).fill(0);

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
    stringtodate(str) {
      const y = str.substr(0, 4);
      const m = str.substr(5, 2);
      const d = str.substr(8, 2);
      return new Date(y, m - 1, d);
    },
  },
};
</script>

<style scoped>
.detail-tel {
  font-size: 14px;
}
.detail-address {
  font-size: 12px;
}
.schedule-name {
  font-size: 20px;
  font-weight: bold;
}
.small-margin {
  margin: 0px 5px;
}
.icon-active {
  color: blue;
}
.icon-no-active {
  color: gray;
}
</style>