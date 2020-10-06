<template>
  <div id="app" style='font-family: "NIXGONM-Vb";'>
    <div v-if="isMobile" style="width: 100%">
      <router-view class="router-view" />
      <Navbar />
    </div>
    <div id="forPcDiv" v-else style="" class="mx-auto maxi-size">
      <router-view class="router-view" />
      <Navbar />
    </div>
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
    return {
      isMobile: window.innerWidth < 600,
    };
  },
  mounted() {
    window.addEventListener("resize", this.setSize);
  },

  methods: {
    setSize() {
      let size = window.innerWidth;
      if (size > 600) {
        this.isMobile = false;
      } else {
        this.isMobile = true;
      }
    },
  },
};
</script>

<style scoped>
.router-view {
  margin-bottom: 100px;
}
.maxi-size {
  width: 600px;
  min-height: 100vh;
}
</style>
