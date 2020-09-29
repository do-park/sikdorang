<template>
  <div>
    <h1>동행 상세보기</h1>
    <div v-if="todaySchedule">
      <h4>{{ todaySchedule.name }}</h4>
      날짜: {{ todaySchedule.date }} <br />
      <button
        v-if="stringtodate(todaySchedule.date) > today"
        class="btn btn-primary"
      >
        동행 신청하기
      </button>
      <button v-else class="btn btn-secondary disabled">
        이미 지나간 일정입니다.
      </button>
      <!-- 지도 -->
      <h3>일정</h3>
      {{ trip.plan }}
      <div v-for="(schedule, index) in todaySchedule.schedules" :key="index">
        [{{ schedule.type }}] {{ schedule.store_name }}{{ schedule.name }} |
        {{ schedule.address }}
      </div>
      <h3>설명</h3>
      {{ todaySchedule.content }}
    </div>
  </div>
</template>

<script>
export default {
  name: "PartyListItemDetail",
  data() {
    return {
      party: this.$cookies.get("party"),
      trip: this.$cookies.get("trip"),
      todaySchedule: { name: "", date: "", schedules: [], content: "" },
      today: "",
    };
  },
  mounted() {
    console.log(this.party);
    console.log(this.trip);
    this.makeScheduleList();
    this.today = new Date();
  },
  methods: {
    //일정 정보 가져오면 스케줄 리스트로 만들기
    makeScheduleList() {
      this.todaySchedule.name = this.trip.name;
      this.todaySchedule.date = this.trip.date;
      this.todaySchedule.content = this.party.content;
      //일정 리스트로 만들기
      const plans = this.trip.plan.split("-");

      plans.forEach((plan, index) => {
        console.log(index);
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
              // this.todaySchedule.schedules.push(result);
              // this.todaySchedule.schedules[index] = result;
              this.$set(this.todaySchedule.schedules, index, result);
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

              // this.todaySchedule.schedules.push({
              //   id: items.contentid,
              //   name: items.title,
              //   branch: "",
              //   tel: items.tel,
              //   address: items.addr1 + items.addr2,
              //   latitude: items.mapy,
              //   longtitude: items.mapx,
              //   //category가 있지만, 식당/카페와 동일하게&혼선 안되게 하기 위해 type을 또 넣음.
              //   type: `${typeName}`,
              //   category: `${typeName}`,
              //   tags: "",
              //   img: items.firstimage,
              // });
              // this.todaySchedule.schedules[index] = {
              //   id: items.contentid,
              //   name: items.title,
              //   branch: "",
              //   tel: items.tel,
              //   address: items.addr1 + items.addr2,
              //   latitude: items.mapy,
              //   longtitude: items.mapx,
              //   //category가 있지만, 식당/카페와 동일하게&혼선 안되게 하기 위해 type을 또 넣음.
              //   type: `${typeName}`,
              //   category: `${typeName}`,
              //   tags: "",
              //   img: items.firstimage,
              // };
              this.$set(this.todaySchedule.schedules, index, {
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