<template>
  <v-app>
    <v-main>
      <router-link to="/">Home</router-link>|
      <router-link to="/maptest">MapTest</router-link>|
      <router-link to="/map">Map 시작하기</router-link>|
      <router-link to="/idealtagcup">이상형 월드컵 테스트</router-link>|
      <router-link to="/schedule">schedule</router-link>|
      <router-link to="/recommend">recommend</router-link>|
      <span v-if="$store.state.isLogin"><a @click="tryLogout">로그아웃</a></span>
      <router-view />
    </v-main>
  </v-app>
</template>

<script>
export default {
  name: "App",
  data() {
    return {
      
    }
  },
  methods: {
    tryLogout() {
      window.$cookies.remove('auth-token')
      this.$store.state.isLogin = false

      //get으로 로그아웃 보내기 (헤더에 토큰)

      // 로그아웃이 완료되면 사용자를 홈페이지로 던집니다.
			this.$router.push({ name: 'Home' })
			window.location.reload()

    }
  },
};
</script>
