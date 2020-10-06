<template>
  <div>
    <div id="recommendcontainer">
      <div v-if="!isLogin" id="loginRec" class="d-flex flex-column align-items-center justify-content-center" @click="onLoginRecClick()">
        <img class="logo" src="@/assets/sikdoranglogo.png" alt="">
        <p class="h4">여행을 시작할까요?</p>
      </div>
      <div v-else>
        <div id="recommendLoc" class="mt-3" @click="clickRecommend">
          <Recommend :username="username" />
        </div>
        <div id="mypick">
          <button class="long-btn" @click="clickMyChoice">
            <div>내가 일정 골라서 떠날래요 <i class="fas fa-car-side"></i></div>
          </button>
        </div>
      </div>
    </div>
    <div id="themepick" class="theme-wrap m-4">
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
            location.reload()
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
    onLoginRecClick() {
      this.$router.push({ name: "Login" })
    }
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
.long-btn{
  max-width: 600px;
  width: 90vw;
  height: 60px;
  background: white;
  border-radius: 0.8rem;
  border : 3px solid crimson;
}
.main-btn {
  width: 500px;
  height: 80px;
}
#recommendLoc{
  height : 28vh;
}
#mypick{
  margin-top: 2vh;
  margin-bottom: 9vh;
  font-size : 18px;
  font-weight: bold;
}
#loginRec{
  background-image: url("/assets/sikdoranglogo.png");
  height: 50vh;
}
.logo {
  width: 80%;
}
</style>
