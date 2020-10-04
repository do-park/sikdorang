<template>
  <nav class="text-center">
    <div class="fixed-bottom wrap row">
      <div class="center-btn">
        <div v-if="isLogin && (currentRouteName === 'Home')" class="row m-0 sikdorang" @click="toMyPage">
          <img class="user-profile-img" :src="imgSrc" alt="user profile image">
        </div>
        <div v-else class="row m-0 sikdorang" @click="toMain"><i class="fas fa-home fa-2x m-auto"></i></div>
      </div>
      <div class="col-6 p-0 my-auto" @click="toTour"><i class="fas fa-flag fa-2x"></i></div>
      <div class="col-6 p-0 my-auto" @click="toParty"><i class="fas fa-users fa-2x"></i></div>
    </div>
  </nav>
</template>

<script>
import { mapGetters } from "vuex"
const mypage = "mypage"

export default {
  name: "Navbar",
  data() {
    return {
      isLogin: this.$store.state.isLogin,
    };
  },
  computed: {
    ...mapGetters(mypage, [
      'getUserInfo'
    ]),
    imgSrc() {
        console.log(this.getUserInfo.profile_image)
        return this.getUserInfo.profile_image
    },
    currentRouteName() {
        return this.$route.name;
    }
  
  },

  methods: {
    toTour() {
      this.$router.push('/trip/list')
    },
    toMyPage() {
      this.$router.push('/mypage')
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
.user-profile-img {
  display: block;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  margin: auto;

  background-repeat: no-repeat;
  background-position: center center;
  background-size: cover;
} 
.wrap {
  height: 50px;
  max-width: 600px;
  margin: 0px auto;
  background-color: crimson;
  color: white !important;
}
.center-btn {
  position: absolute;
  z-index: 1;
  left: 50%;
  transform: translateX(-50%);
}
.sikdorang {
  height: 50px;
  width: 50px;
  border-radius: 50%;
  background: black;
}
</style>
