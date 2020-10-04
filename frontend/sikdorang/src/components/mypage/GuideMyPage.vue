<template>
  <div class="guide-tour">
    <div class="tour-text">상품 관리</div>
    <div class="btn-wrap">
      <button class="create-btn" @click="createItem">상품 등록하기</button>
    </div>
    <div v-if="(guideItems.length > 0)" class="margin-x">
      <div v-for="item in guideItems" :key="item.id">
        <GuideMyPageItem :item="item" />
      </div>
    </div>
    <div v-else class="margin-x">
      <div>등록한 상품이 없습니다.</div>
    </div>

  </div>
</template>

<script>
import GuideMyPageItem from './GuideMyPageItem.vue'
import { mapGetters } from "vuex"
const mypage = "mypage"

export default {
  name: "GuideMyPage",
  components: {
    GuideMyPageItem,
  },
  data() {
    return {
      guideItems: [],
    }
  },
  computed: {
    ...mapGetters(mypage, [
      'getUserInfo'
    ]),
  },
  mounted() {
    this.getTourItems()
  },
  methods: {
    createItem() {
      this.$router.push('/trip/createchedule')
    },
    getTourItems() {
      const requestHeaders = {
        headers: {
          Authorization: `JWT ${this.$cookies.get("auth-token")}`,
        },
      };
      const target = this.getUserInfo.username
      this.$axios
      .get(`/guide/list/${target}`, requestHeaders)
      .then((res) => {
        res.data.forEach((target, index) => {
          const stringDate = target.start_date.toString()
          res.data[index].start_date = `${stringDate.substr(0,4)}년 ${stringDate.substr(4,2)}월 ${stringDate.substr(6,2)}일`
          const stringDate2 = target.end_date.toString()
          res.data[index].end_date = `${stringDate2.substr(0,4)}년 ${stringDate2.substr(4,2)}월 ${stringDate2.substr(6,2)}일`
          res.data[index].title_img = this.$store.state.IMG_SERVER_URL + res.data[index].title_img
        })
        this.guideItems = res.data
      })
      .catch((err) => {
        console.log(err);
      });
    },
  },
  
}
</script>

<style scoped>
.guide-tour {
  position: relative;
  border: 2px dotted crimson;
  border-radius: 20px;
  margin: 0px 5px;
  min-height: 200px;
}
.tour-text {
  background-color: white;
  padding: 5px 35px 0px;
  font-size: 14px;
  font-weight: bolder;
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  margin-bottom: -10px;
  top: -20px;
}
.btn-wrap {
  margin: 1rem;
  text-align: right;
}
.create-btn {
  background-color: crimson;
  padding: 8px;
  font-size: 12px;
  color: white;
  border-radius: 10px;
}
.margin-x {
  margin: 1rem 5px;
}
</style>