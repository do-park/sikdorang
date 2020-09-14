<template>
  <v-app>
    <v-main>
      <router-link to="/idealtagcup">이상형 월드컵 테스트</router-link>
      <router-view/>
    </v-main>
  </v-app>
</template>

<script>
export default {
  name: "App",

  components: {
  },

  data: () => ({
    //
  }),
};
</script>
