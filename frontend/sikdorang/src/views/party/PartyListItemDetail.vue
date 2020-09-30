<template>
  <div>
    <h1>동행 상세보기</h1>
    <div v-if="tripSchedule">
      <h4>제목: {{ tripSchedule.name }}</h4>
      날짜: {{ tripSchedule.date }} <br />
      <button
        v-if="stringtodate(tripSchedule.date) > today"
        class="btn btn-primary"
        @click="onClick()"
      >
        동행 신청하기
      </button>
      <button v-else class="btn btn-secondary disabled">
        이미 지나간 일정입니다.
      </button>
      <h4>map something</h4>
      <!-- <MapMain /> -->
      <h3>일정</h3>
      <div v-for="(schedule, index) in tripSchedule.schedules" :key="index">
        [{{ schedule.type }}] {{ schedule.store_name }}{{ schedule.name }} |
        {{ schedule.address }}
      </div>
      <h3>설명</h3>
      {{ tripSchedule.content }}
    </div>
  </div>
</template>

<script>
// import MapMain from "@/views/MapMain.vue";
import Swal from "sweetalert2";

export default {
  name: "PartyListItemDetail",
  components: {
    // MapMain,
  },
  data() {
    return {
      party: this.$cookies.get("party"),
      trip: this.$cookies.get("trip"),
      tripSchedule: { name: "", date: "", schedules: [], content: "" },
      today: "",
    };
  },
  mounted() {
    this.makeScheduleList();
    this.today = new Date();
  },
  methods: {
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
            longtitude: items.mapx,
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
      this.tripSchedule.name = this.trip.name;
      this.tripSchedule.date = this.trip.date;
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
    onClick() {
      Swal.fire({
        title: "동행 신청하기",
        input: "textarea",
        inputPlaceholder:
          "휴대폰 번호, 카카오톡 아이디 등 연락처를 포함한 한마디를 전하세요.",
        showCancelButton: true,
      }).then((result) => {
        console.log(result.value);
        const requestHeaders = {
          headers: {
            Authorization: `JWT ${this.$cookies.get("auth-token")}`,
          },
        };
        this.$axios
          .post(
            `party/create_message/${this.party.id}`,
            result.value,
            requestHeaders
          )
          .then((res) => {
            console.log(res);
            // 등록이 완료되면 상세페이지로 이동
            // this.$router.push(`주소`);
          })
          .catch((err) => console.error(err));
      });
    },
  },
};
</script>

<style>
</style>