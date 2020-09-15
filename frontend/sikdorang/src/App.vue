<template>
  <v-app>
    <v-main>
      <router-link to="/">Home</router-link> |
      <router-link to="/maptest">MapTest</router-link> |
      <router-link to="/map">Map 시작하기</router-link> |
      <router-link to="/signup">Signup</router-link> |
      <router-view/>
    </v-main> 
  </v-app>
</template>

<script>

export default {
  name: "App",

  data: () => ({

  }),
};
</script>
