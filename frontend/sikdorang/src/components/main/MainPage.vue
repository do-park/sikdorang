<template>
  <div>
    <div id="recommendcontainer">
      <div v-if="!isLogin">
        <h4 class="d-inline-block my-auto txt">여행을 시작할까요?</h4>
      </div>
      <div id="recommendLoc" @click="clickRecommend">
        <Recommend :username="username" />
      </div>
    </div>
    <div>
      <div id="mypick">
        <button class="long-btn" @click="clickMyChoice">
          <div>내가 일정 골라서 떠나볼래요 <i class="fas fa-car-side"></i></div>
        </button>
      </div>
      <div id="themepick" class="theme-wrap m-4">
        <ThemePage />
      </div>

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
    console.log(this);
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
      console.log("2번", true);
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
.long-btn{
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
  margin-top: 9vh;
  margin-bottom: 9vh;
  font-size : 18px;
  font-weight: bold;
}


</style>
