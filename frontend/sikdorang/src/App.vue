<template>
  <div id="app">
      <router-link to="/">Home</router-link>|
      <router-link to="/map">Map 시작하기</router-link>|
      <router-link to="/idealtagcup">이상형 월드컵 테스트</router-link>|
      <router-link to="/schedule">schedule</router-link>|
      <router-link to="/recommend">recommend</router-link>|
      <router-link to="/test">test</router-link>|
      <span v-if="$store.state.isLogin"><a @click="tryLogout">로그아웃</a></span>
      <router-view />
  </div>
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

      console.log(this.$cookies.get('auth-token'))

      const requestHeaders = {
        headers: {
          Authorization: `JWT ${this.$cookies.get('auth-token')}`
        }
      }

      //get으로 로그아웃 보내기 (헤더에 토큰)
      this.$axios.post(`/rest-auth/logout/`, requestHeaders)
      .then (response => {
        console.log(response)
        // 로그아웃이 완료되면 사용자를 홈페이지로 던집니다.
        this.$router.push({ name: 'Home' })
        window.location.reload()
      })
      .catch(err => {
        console.log(err)
      })

    }
  },
};
</script>
