<template>
  <div>
    <hr />
    <div v-if="!isLogin">여행을 시작할까요?</div>
    <div v-else class="text-left">
      <h3>{{ username }}님,</h3>
      <div class="d-flex justify-content-center">
        <h3 class="text-center"><Recommend /></h3>
      </div>
      <h3 class="text-right">어떠세요?</h3>
    </div>
    <hr />
    <div class="btn-wrap row m-0 justify-content-around">
      <div class="w-100 col-4">
        <button class="btn btn-danger main-btn" @click="clickMyChoice">
          <div>내가</div>
          <div>고르기</div>
        </button>
      </div>
      <div class="w-100 col-4">
        <button
          class="btn btn-danger main-btn d-inline-block"
          @click="clickRecommend"
        >
          <div>식도랑</div>
          <div>추천코스</div>
        </button>
      </div>
    </div>
    <hr />
    <ThemePage />
    <hr />
    <button class="btn btn-primary" @click="clickToLoginPageOrMyPage">
      {{ loginOrMypage }}
    </button>
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
</style>
