<template>
  <div>
    <div>투어 상품 관리</div>
    <button class="btn btn--primary" @click="createItem">상품 등록하기</button>
    <div v-for="item in guideItems" :key="item.id">
      <GuideMyPageItem :item="item" />
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

<style>

</style>