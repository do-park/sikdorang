<template>
  <div class="home">
    <v-btn  v-if="!nowMain" class="arrow-btn" color="primary" @click="changeToMainPage">지금은 로그인페이지</v-btn>
    <transition name="component-fade" mode="out-in">
      <component v-bind:is="view"></component>
    </transition>
    <v-btn  v-if="nowMain" class="arrow-btn" color="primary" @click="changeToLoginPage">지금은 메인페이지</v-btn>
  </div>
</template>

<script>
// @ is an alias to /src
import MainPage from '@/components/main/MainPage.vue'
import LoginPage from '@/components/main/LoginPage.vue'

export default {
  name: 'Home',
  components: {
    MainPage,
    LoginPage
  },
  data() {
    return {
      view: MainPage,
      nowMain: true
    }
  },
  methods: {
    changeToLoginPage() {
      this.view = LoginPage
      this.nowMain = false
    },

    changeToMainPage() {
      this.view = MainPage
      this.nowMain = true
    }
  },
}
</script>

<style scope>
  .component-fade-enter-active, .component-fade-leave-active {
    transition: all 0.5s;
  }
  .component-fade-enter {
    opacity: 0;
    transform: translateY(30px);
  }
  .component-fade-leave-to {
    opacity: 0;
    transform: translateY(-30px);
  }
  .home {
    text-align: center;
  }
  .arrow-btn {
    margin: auto;
  }
</style>