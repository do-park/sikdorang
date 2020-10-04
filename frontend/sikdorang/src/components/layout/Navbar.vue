<template>
  <nav class="text-center">
    <div class="fixed-bottom wrap row">
      <div to="/trip/list" class="col-5 p-0 my-auto" @click="toTour">투어아이콘</div>
      <div to="/" class="col-2 p-0 row m-0 sikdorang" @click="toMain"><i class="fas fa-home fa-2x m-auto"></i></div>
      <div to="/party/list" class="col-5 p-0 my-auto" @click="toParty">동행아이콘</div>
    </div>
  </nav>
</template>

<script>

export default {
  name: "Navbar",
  data() {
    return {};
  },
  methods: {
    toTour() {
      this.$router.push('/trip/list')
    },
    toMain() {
      this.$router.push('/')
    },
    toParty() {
      this.$router.push('/party/list')
    }
  },
};
</script>

<style scoped>

.wrap {
  height: 50px;
  max-width: 600px;
  margin: 0px auto;
  background-color: crimson;
  color: white !important;
}
.sikdorang {
  height: 50px;
  border-radius: 50%;
  background: black;
}
</style>
