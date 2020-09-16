<template>
  <div id="app">
      <router-link to="/">Home</router-link>|
      <router-link to="/maptest">MapTest</router-link>|
      <router-link to="/map">Map 시작하기</router-link>|
      <router-link to="/idealtagcup">이상형 월드컵 테스트</router-link>
      <router-link to="/signup">Signup</router-link>|
      <router-link to="/schedule">schedule</router-link>
      <router-view />
  </div>
</template>

<script>
export default {
  name: "App",

  data: () => ({}),
};
</script>
