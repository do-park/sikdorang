<template>
  <div id="app">
    <Navbar />
    <router-view />
  </div>
</template>

<script>
import Navbar from "../src/components/layout/Navbar.vue";

export default {
  name: "App",
  components: {
    Navbar,
  },
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
