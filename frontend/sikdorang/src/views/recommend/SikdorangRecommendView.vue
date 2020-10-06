<template>
  <div>
    <div style="height: 10vh"></div>
    <h3 class="text-center">맛집을 찾는 중</h3>
    <div style="height: 5vh"></div>
    <div class="container fa-4x">
      <div class="row justify-content-center">
        <i class="fas fa-cookie-bite fa-spin" style="color: brown"></i>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
import axios from "axios";

const CATEGORY_NAME = [
  "한식",
  "분식",
  "피자",
  "치킨",
  "돈가스/회/일식",
  "카페/디저트/베이커리",
  "아시안",
  "양식",
  "중식",
  "도시락",
  "패스트푸드",
  "술집",
  "족발/보쌈",
  "찜/탕",
];

export default {
  name: "SikdorangRecommendView",
  computed: {
    ...mapGetters("sikRec", ["getForUser"]),
    ...mapGetters("schedule", ["getSchedules"]),
  },
  data() {
    return {
      schedules: [],
      beforeLat: null,
      beforeLng: null,
      beforeCat: [],
    };
  },
  methods: {
    ...mapActions("mapEvent", ["actionPlanList"]),
    divideRecommendation(cf, index) {
      if ((cf === "식당") | (cf === "카페")) {
        this.getSCRecommendation(cf, index);
      } else {
        this.getSHRecommendation(cf, index);
      }
    },
    getRandomInt(min, max) {
      min = Math.ceil(min);
      max = Math.floor(max);
      return Math.floor(Math.random() * (max - min)) + min; //최댓값은 제외, 최솟값은 포함
    },
    async getSCRecommendation(cf, index) {
      const requestHeaders = {
        headers: {
          Authorization: `JWT ${this.$cookies.get("auth-token")}`,
        },
      };
      await this.$axios
        .post(
          "recommend/tag-recommend/",
          {
            category: cf,
            lat: this.beforeLat,
            lng: this.beforeLng,
            bc: this.beforeCat,
          },
          requestHeaders
        )
        .then((res) => {
          const result = res.data.result[0];
          this.schedules[index].userChoice = result;
          this.beforeLat = result.latitude;
          this.beforeLng = result.longitude;
          this.beforeCat.push(result.category);
        })
        .catch((err) => console.error("알고리즘 추천 실패", err));
    },
    async getSHRecommendation(cf, index) {
      const TOUR_API_KEY =
        "K%2FplKHR5Hx7sLQwMexw4LCgDz45JjMDfJ1czEyCx83EBoZHJLUOKe%2B56J93QhZ41DlYmdRy3b1LIpwlSh%2FxYfQ%3D%3D";
      let contentTypeId = 32;
      if (cf === "관광지") {
        contentTypeId = 12;
      }
      await axios
        .get(
          `http://api.visitkorea.or.kr/openapi/service/rest/KorService/locationBasedList?ServiceKey=${TOUR_API_KEY}&contentTypeId=${contentTypeId}&mapX=${this.beforeLng}&mapY=${this.beforeLat}&radius=5000&listYN=Y&MobileOS=ETC&MobileApp=TourAPI3.0_Guide&arrange=A&numOfRows=12&pageNo=1&_type=json`
        )
        .then((res) => {
          const items = res.data.response.body.items.item;
          let idx = this.getRandomInt(0, items.length);
          this.schedules[index].userChoice = {
            id: items[idx].contentid,
            store_name: items[idx].title,
            branch: "",
            tel: items[idx].tel,
            address: items[idx].addr1 + items[idx].addr2,
            latitude: items[idx].mapy,
            longitude: items[idx].mapx,
            category: cf,
            tags: "",
            img: items[idx].firstimage,
          };
          this.beforeLat = this.schedules[index].userChoice.latitude;
          this.beforeLng = this.schedules[index].userChoice.longitude;
          this.beforeCat.push(this.schedules[index].userChoice.category);
        })
        .catch((err) => console.error(err));
    },
  },
  async mounted() {
    this.schedules = this.getSchedules;
    this.beforeLat = this.getForUser.latitude;
    this.beforeLng = this.getForUser.longitude;
    for (let i = 0; i < this.schedules.length; i++) {
      if (i == 0) {
        const forUser = this.getForUser;
        this.schedules[i].userChoice = {
          id: forUser.id,
          store_name: forUser.store_name,
          branch: forUser.branch,
          tel: forUser.tel,
          address: forUser.address,
          latitude: forUser.latitude,
          longitude: forUser.longitude,
          category: CATEGORY_NAME[forUser.category],
          tags: forUser.tags,
        };
      } else {
        await this.divideRecommendation(this.schedules[i].name, i);
      }
    }
    this.actionPlanList(this.schedules);
    setTimeout(() => {
      this.$router.replace("/mypage");
    }, 3000);
    // 생성 완료
  },
};
</script>

<style>
</style>