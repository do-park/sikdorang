<template>
  <div class="home">
    <MainPage />
    <LoginPage />
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
  }
}
</script>
