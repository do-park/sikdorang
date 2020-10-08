<template>
  <div v-if="tripSchedule">
    <div style="height: 5vh"></div>
    <div>
      <h3 class="text-center custom-break-word">{{ tripSchedule.name }}</h3>
      <div class="m-3">
        <div class="date text-center custom-break-word">
          {{ tripSchedule.date.toString().substr(0, 4) }}년 
          {{ tripSchedule.date.toString().substr(4, 2) }}월 
          {{ tripSchedule.date.toString().substr(6, 2) }}일
        </div>
        <div class="date text-center custom-break-word">
          '{{ party.user.username }}'님과 함께해요!
        </div>
      </div>
      <div v-if="party.user.username !== username" class="row justify-content-center m-3">
        <button
          class="default-btn"
          @click="createMessage()"
        >
          연락하기
        </button>
      </div>
      <div v-else class="row justify-content-between m-3">
        <button class="col-12 p-0 btn btn-outline-danger" @click="deleteParty()">
          삭제하기
        </button>
      </div>
    </div>
    <hr>
    <viewer
      v-if="tripSchedule.content"
      :initialValue="tripSchedule.content"
      class="mx-3"
    />
    <hr>
    <div class="m-3">
      <MyPageMap :todaySchedule="tripSchedule.schedules" />
    </div>
    <div class="m-3">
      <div v-for="(schedule, index) in tripSchedule.schedules" :key="index">
        <div class="row schedule-detail m-0">

          <div class="col-12 p-0 row m-0">
            <div class="col-1 p-0">
              <i v-if="(schedule.type === '식당')" class="fas fa-utensils" style="color: tomato"></i>
              <i v-else-if="(schedule.type === '카페')" class="fas fa-coffee" style="color: sienna"></i>
              <i v-else-if="(schedule.type === '관광지')" class="fas fa-place-of-worship" style="color: steelblue"></i>
              <i v-else class="fas fa-bed" style="color: seagreen"></i>
            </div>
            <div class="col-6 p-0 font-weight-bold">
              <div v-if="(schedule.type === '식당') | (schedule.type === '카페')" class="text-truncate">{{ schedule.store_name }}</div>
              <div v-else class="text-truncate">{{ schedule.name }}</div>
            </div>
            <div class="col-5 p-0 detail-tel text-right">{{schedule.tel}}</div>
            <div class="col-12 p-0 detail-address">{{schedule.address}}</div>
          </div>
        </div>
        <div class="my-1 text-center"></div>
      </div>
    </div>
  </div>
</template>

<script>
// import MapMain from "@/views/MapMain.vue";
import Swal from "sweetalert2";
import MyPageMap from "@/components/mypage/MyPageMap.vue";
import "@toast-ui/editor/dist/toastui-editor-viewer.css";
import { Viewer } from "@toast-ui/vue-editor";
import { mapGetters } from "vuex";
const party = "party";

export default {
  name: "PartyListItemDetail",
  components: {
    viewer: Viewer,
    MyPageMap,
    // MapMain,
  },
  data() {
    return {
      username: this.$cookies.get("username"),
      party: null,
      trip: null,
      tripSchedule: { name: "", date: "", schedules: [], content: "" },
    };
  },
  computed: {
    ...mapGetters(party, ["getParty", "getTrip"]),
  },
  created() {
    this.party = this.getParty;
    this.trip = this.getTrip;
    this.makeScheduleList();
  },
  methods: {
    async restuarantPlan(i, id, type, typeName) {
      this.$axios
        .get(`/trip/store_detail/${id}`)
        .then((res) => {
          const result = res.data;

          //가게의 타입도 구분
          if (type === "C") {
            typeName = "카페";
          }
          result["type"] = typeName;
          this.$set(this.tripSchedule.schedules, i, result);
          return result;
        })
        .catch((err) => {
          console.error(err);
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
            name: items.title,
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
          this.$set(this.tripSchedule.schedules, i, result);
          return result;
        })
        .catch((err) => {
          console.error(err);
          return [];
        });
    },
    //일정 정보 가져오면 스케줄 리스트로 만들기
    async makeScheduleList() {
      this.tripSchedule.name = this.party.title;
      this.tripSchedule.date = this.party.trip_date;
      this.tripSchedule.content = this.party.content;

      //일정 리스트로 만들기
      const plans = this.trip.plan.split("-");
      this.tripSchedule.schedules = new Array(plans.length).fill(0);

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
    createMessage() {
      Swal.fire({
        title: "연락하기",
        input: "textarea",
        inputPlaceholder:
          "휴대폰 번호, 카카오톡 아이디 등 연락처를 포함한 한마디를 전하세요.",
        showCancelButton: true,
        confirmButtonColor: "crimson",
        cancelButtonColor: "gray",
      }).then((res) => {
        if (res.isConfirmed) {
          const requestHeaders = {
            headers: {
              Authorization: `JWT ${this.$cookies.get("auth-token")}`,
            },
          };
          this.$axios
            .post(
              `/party/create_message/${this.party.id}`,
              { content: res.value },
              requestHeaders
            )
            .then(() => {
              Swal.fire({
                icon: "success",
                title: "메시지를 전송하였습니다.",
                confirmButtonColor: "crimson",
              });
            })
            .catch((err) => console.error(err));
        }
      });
    },
    updateParty() {
      this.$cookies.set("party-trip-id", this.party.id);
      this.$cookies.set("party", this.party);
      this.$cookies.set("party-trip-date", this.party.trip_date);
      this.$cookies.set("party-type", 1);
      this.$router.push({ name: "PartyForm" });
    },
    deleteParty() {
      Swal.fire({
        icon: "warning",
        title: "게시글 삭제",
        text: "게시글을 삭제하시겠습니까?",
        showCancelButton: true,
        confirmButtonText: "삭제합니다.",
        confirmButtonColor: "crimson",
        cancelButtonColor: "gray",
      }).then((result) => {
        if (result.isConfirmed) {
          const requestHeaders = {
            headers: {
              Authorization: `JWT ${this.$cookies.get("auth-token")}`,
            },
          };

          this.$axios
            .delete(`/party/delete/${this.party.id}`, requestHeaders)
            .then(() => {
              Swal.fire({
                icon: "success",
                title: "삭제했습니다.",
                confirmButtonColor: "crimson",
              }).then(() => {
                this.$router.push({ name: "PartyList" });
              });
            })
            .catch((err) => console.error(err));
        }
      });
    },
  },
};
</script>

<style>
.swal2-popup {
  font-family: "NIXGONM-Vb";
  font-size: 0.7rem !important;
}
.date {
  font-size: 14px;
}
.default-btn {
  color: white;
  background-color: crimson;
  padding: 0.5rem 1rem;
  border-radius: 1rem;
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
</style>