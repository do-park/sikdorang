<template>
  <div>
    <button class="btn btn-primary" @click="clickToMainPage">메인으로</button>
    <div class="login-wrap p-2">
      <h3 class="my-4">로그인</h3>
      <div class="row m-0">
        <div class="col-9 p-0 pr-1">
          <input
            type="text"
            class="form-control"
            v-model="loginData.username"
            placeholder="아이디"
            hide-details="auto"
          />
          <input
            type="password"
            class="form-control"
            v-model="loginData.password"
            placeholder="비밀번호"
          />
        </div>
        <button class="btn btn-secondary login-btn col-3" @click="clickLogin">
          로그인
        </button>
      </div>
      <div class="mt-3">
        <router-link to="/signup" class="text-dark"
          >아직 회원이 아니세요?</router-link
        >
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions } from "vuex";

export default {
  name: "LoginPage",
  data() {
    return {
      isLogin: this.$store.state.isLogin,
      loginData: {
        username: "",
        password: "",
      },
    };
  },
  methods: {
    ...mapActions("mypage", ["actionUserInfo"]),
    clickLogin() {
      this.$axios
        .post(`/rest-auth/login/`, this.loginData)
        .then((response) => {
          // console.log(response)
          window.$cookies.set("auth-token", response.data.token);
          this.$store.state.isLogin = true;
          this.actionUserInfo(response.data.user);
          if (response.data.user.done_cup === 1) {
            this.$router.push("/");
          } else {
            this.$router.push("/idealtagcup");
          }
        })
        .catch((err) => {
          console.log(err);
          alert("아이디 또는 비밀번호를 다시 확인해주세요.");
        });
    },
    clickToMainPage() {
      this.$emit("toMainPage");
    },
  },
};
</script>

<style scoped>
.login-wrap {
  background-color: lightsalmon;
  border-radius: 1rem;
}
.login-btn {
  float: right;
  height: 76px;
}
</style>
