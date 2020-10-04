<template>
  <div>
    <div>투어 상품 관리</div>
    <div>ddd</div>

  </div>
</template>

<script>
import { mapGetters } from "vuex"
const mypage = "mypage"

export default {
  name: "GuideMyPage",
  components: {
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