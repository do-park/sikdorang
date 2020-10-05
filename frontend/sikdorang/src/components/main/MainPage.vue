<template>
  <div>
    <div v-if="!isLogin" class="main-ment p-5">
      <h5 class="d-inline-block my-auto">여행을 시작할까요?</h5>
    </div>
    <div v-else class="main-ment text-left p-5">
      <h5>{{ username }}님,</h5>
      <div class="d-flex justify-content-center">
        <h4 class="text-center"><Recommend /></h4>
      </div>
      <h5 class="text-right">어떠세요?</h5>
    </div>
    <div class="btn-wrap row m-0 mb-5 p-0 justify-content-center">
      <div class="col-5 m-0 p-0">
        <button class="btn btn-danger main-btn" @click="clickMyChoice">
          <div>내가</div>
          <div>고르기</div>
        </button>
      </div>
      <div class="col-5 m-0 p-0">
        <button class="btn btn-danger main-btn" @click="clickRecommend">
          <div>식도랑</div>
          <div>추천코스</div>
        </button>
      </div>
    </div>
    <div class="theme-wrap">
      <ThemePage />
    </div>
  </div>
</template>

<script>
import ThemePage from "@/components/main/ThemePage.vue";
import Recommend from "@/views/Recommend.vue";
import { mapActions } from "vuex";

export default {
  name: "MainPage",
  data() {
    return {
      loginOrMypage: "로그인",
      isLogin: this.$store.state.isLogin,
      username: "",
    };
  },
  mounted() {
    this.actionIsSik(false);
    if (this.$store.state.isLogin) {
      const requestHeaders = {
        headers: {
          Authorization: `JWT ${this.$cookies.get("auth-token")}`,
        },
      };
      this.$axios
        .get(`/rest-auth/user`, requestHeaders)
        .then((res) => {
          this.username = res.data.username;
          this.$cookies.set("username", this.username);
        })
        .catch((err) => {
          console.error(err);
          if (this.isLogin) {
            this.$store.state.isLogin = false;
            this.isLogin = false;
            this.loginOrMypage = "로그인";
          }
        });
      this.loginOrMypage = "마이페이지";
    }
  },
  components: {
    ThemePage,
    Recommend,
  },
  methods: {
    ...mapActions("sikRec", ["actionIsSik"]),
    clickMyChoice() {
      this.$router.push({ name: "Schedule" });
    },
    clickRecommend() {
      this.actionIsSik(true);
      this.$router.push({ name: "Schedule" });
    },
    clickToLoginPageOrMyPage() {
      this.$emit("toLoginPageOrMyPage");
    },
  },
};
</script>

<style scoped>
.main-wrap {
  width: 400px;
  height: 500px;
  margin-left: auto;
  margin-right: auto;
  text-align: center;
}

.main-btn {
  width: 100px;
  height: 100px;
}
.main-ment {
  height: 40vh;
  margin: auto;
}
</style>
