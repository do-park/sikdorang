<template>
  <div>
    <nav class="navbar navbar-expand-xl navbar-dark bg-primary">
      <a class="navbar-brand" href="#">Navbar</a>
      <button
        class="navbar-toggler"
        type="button"
        data-toggle="collapse"
        data-target="#navbarNavAltMarkup"
        aria-controls="navbarNavAltMarkup"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
        <div class="navbar-nav">
          <router-link to="/">Home</router-link>
          <router-link to="/idealtagcup">이상형 월드컵 테스트</router-link>
          <router-link to="/schedule">schedule</router-link>
          <router-link to="/recommend">recommend</router-link>
          <router-link to="/trip/list">여행 리스트</router-link>
          <router-link to="/trip/createchedule">여행 생성(가이드)</router-link>
          <router-link to="/rectest">태그추천</router-link>
          <span v-if="$store.state.isLogin"
            ><a @click="tryLogout">로그아웃</a></span
          >
        </div>
      </div>
    </nav>
  </div>
</template>

<script>
export default {
  name: "Navbar",
  data() {
    return {};
  },
  methods: {
    tryLogout() {
      window.$cookies.remove("auth-token");
      this.$store.state.isLogin = false;

      console.log(this.$cookies.get("auth-token"));

      const requestHeaders = {
        headers: {
          Authorization: `JWT ${this.$cookies.get("auth-token")}`,
        },
      };

      //get으로 로그아웃 보내기 (헤더에 토큰)
      this.$axios
        .post(`/rest-auth/logout/`, requestHeaders)
        .then((response) => {
          console.log(response);
          // 로그아웃이 완료되면 사용자를 홈페이지로 던집니다.
          this.$router.push({ name: "Home" });
          window.location.reload();
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>

<style></style>
