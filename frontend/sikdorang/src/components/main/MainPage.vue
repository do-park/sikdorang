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
      <div id="mypick" class="my-5">
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
  height : 27vh;
}
#mypick{
  font-size : 18px;
  font-weight: bold;
}
/* #recommendcontainer {
  height: 25vh;
  line-height : 25vh;
  padding : 5vh;
  margin: auto;
} */

/* .content {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  height: 160px;
  overflow: hidden;
  font-family: 'Lato', sans-serif;
  font-size: 35px;
  line-height: 40px;
  color: #ecf0f1;
}
.content__container {
  font-weight: 600;
  overflow: hidden;
  height: 40px;
  padding: 0 40px;
}
.content__container:before {
  content: '[';
  left: 0;
}
.content__container:after {
  content: ']';
  position: absolute;
  right: 0;
}
.content__container:after, .content__container:before {
  position: absolute;
  top: 0;
  color: #16a085;
  font-size: 42px;
  line-height: 40px;
  -webkit-animation-name: opacity;
  -webkit-animation-duration: 2s;
  -webkit-animation-iteration-count: infinite;
  animation-name: opacity;
  animation-duration: 2s;
  animation-iteration-count: infinite;
}
.content__container__text {
  display: inline;
  float: left;
  margin: 0;
}
.content__container__list {
  margin-top: 0;
  padding-left: 110px;
  text-align: left;
  list-style: none;
  -webkit-animation-name: change;
  -webkit-animation-duration: 10s;
  -webkit-animation-iteration-count: infinite;
  animation-name: change;
  animation-duration: 10s;
  animation-iteration-count: infinite;
}
.content__container__list__item {
  line-height: 40px;
  margin: 0;
}
@-webkit-keyframes opacity {
  0%, 100% {
    opacity: 0;
}
  50% {
    opacity: 1;
}
}
@-webkit-keyframes change {
  0%, 12.66%, 100% {
    transform: translate3d(0, 0, 0);
}
  16.66%, 29.32% {
    transform: translate3d(0, -25%, 0);
}
  33.32%, 45.98% {
    transform: translate3d(0, -50%, 0);
}
  49.98%, 62.64% {
    transform: translate3d(0, -75%, 0);
}
  66.64%, 79.3% {
    transform: translate3d(0, -50%, 0);
}
  83.3%, 95.96% {
    transform: translate3d(0, -25%, 0);
}
}
@-o-keyframes opacity {
  0%, 100% {
    opacity: 0;
}
  50% {
    opacity: 1;
}
}
@-o-keyframes change {
  0%, 12.66%, 100% {
    transform: translate3d(0, 0, 0);
}
  16.66%, 29.32% {
    transform: translate3d(0, -25%, 0);
}
  33.32%, 45.98% {
    transform: translate3d(0, -50%, 0);
}
  49.98%, 62.64% {
    transform: translate3d(0, -75%, 0);
}
  66.64%, 79.3% {
    transform: translate3d(0, -50%, 0);
}
  83.3%, 95.96% {
    transform: translate3d(0, -25%, 0);
}
}
@-moz-keyframes opacity {
  0%, 100% {
    opacity: 0;
}
  50% {
    opacity: 1;
}
}
@-moz-keyframes change {
  0%, 12.66%, 100% {
    transform: translate3d(0, 0, 0);
}
  16.66%, 29.32% {
    transform: translate3d(0, -25%, 0);
}
  33.32%, 45.98% {
    transform: translate3d(0, -50%, 0);
}
  49.98%, 62.64% {
    transform: translate3d(0, -75%, 0);
}
  66.64%, 79.3% {
    transform: translate3d(0, -50%, 0);
}
  83.3%, 95.96% {
    transform: translate3d(0, -25%, 0);
}
}
@keyframes opacity {
  0%, 100% {
    opacity: 0;
}
  50% {
    opacity: 1;
}
}
@keyframes change {
  0%, 12.66%, 100% {
    transform: translate3d(0, 0, 0);
}
  16.66%, 29.32% {
    transform: translate3d(0, -25%, 0);
}
  33.32%, 45.98% {
    transform: translate3d(0, -50%, 0);
}
  49.98%, 62.64% {
    transform: translate3d(0, -75%, 0);
}
  66.64%, 79.3% {
    transform: translate3d(0, -50%, 0);
}
  83.3%, 95.96% {
    transform: translate3d(0, -25%, 0);
}
} */

</style>
