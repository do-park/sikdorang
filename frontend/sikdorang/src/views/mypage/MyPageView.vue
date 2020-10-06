<template>
  <transition name="component-fade" mode="out-in">
    <MyPage v-if="isLogin" :isGuide="isGuide" />
  </transition>
</template>

<script>
import { mapActions } from "vuex";
import MyPage from "@/components/mypage/MyPage.vue";
// import GuideMyPage from '@/components/mypage/GuideMyPage.vue'
// import AdminMyPage from '@/components/mypage/AdminMyPage.vue'

export default {
  name: "MyPageView",
  components: {
    MyPage,
    // GuideMyPage,
    // AdminMyPage,
  },
  mounted() {
    const requestHeaders = {
      headers: {
        Authorization: `JWT ${this.$cookies.get("auth-token")}`,
      },
    };
    this.$axios
      .get("rest-auth/user/", requestHeaders)
      .then((res) => {
        this.actionUserInfo(res.data);
        const userCode = res.data.user_code;
        if (userCode === 0) {
          this.isLogin = true;
        } else if (userCode === 1) {
          this.isLogin = true;
          this.isGuide = true;
        } else if (userCode === 2) {
          this.isLogin = true;
          this.isAdmin = true;
        }
        // this.actionTripList(tripItems)
      })
      .catch((err) => console.error(err));
  },
  methods: {
    ...mapActions("mypage", ["actionUserInfo", "actionTripList"]),
  },
  data() {
    return {
      isLogin: false,
      isGuide: false,
      isAdmin: false,
    };
  },
};
</script>

<style scoped>
.component-fade-enter-active {
  transition: all 0.5s;
}
.component-fade-enter {
  opacity: 0;
  transform: translateY(30px);
}
</style>
