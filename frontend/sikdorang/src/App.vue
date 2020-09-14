<template>
  <v-app>
    <v-main>
      <router-link to="/">Home</router-link>|
      <router-link to="/map">map</router-link>|
      <router-link to="/schedule">schedule</router-link>
      <router-view />
    </v-main>
  </v-app>
</template>

<script>
// import MapTest from "./views/MapTest";
// import Schedule from "./views/Schedule";

export default {
  name: "App",

  components: {
    // MapTest,
    // Schedule,
  },

  data: () => ({
    //
  }),
};
</script>
