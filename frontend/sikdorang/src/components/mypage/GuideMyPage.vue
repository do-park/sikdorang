<template>
  <div>
    <div>투어 상품 관리</div>
    <div v-for="item in guideItems" :key="item.id">
      {{ item }}
    </div>

  </div>
</template>

<script>
import { mapGetters } from "vuex"
const mypage = "mypage"

export default {
  name: "GuideMyPage",
  components: {
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
      .then((response) => {
        console.log(response);
        this.guideItems = response.data
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