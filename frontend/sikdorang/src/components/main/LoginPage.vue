<template>
  <div class="login-box">
    <div>로그인 페이지</div>
    <v-text-field
      v-model="loginData.username"
      label="아이디"
      hide-details="auto"></v-text-field>
    <v-text-field
      v-model="loginData.password"
      label="비밀번호"
      :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
      :type="show1 ? 'text' : 'password'"
      @click:append="show1 = !show1"></v-text-field>
    <v-btn 
      class="login-btn" 
      color="primary" 
      @click="clickLogin">로그인</v-btn>
  </div>
</template>

<script>
export default {
  name:'LoginPage',
  data() {
    return {
      isLogin: this.$store.state.isLogin,
      loginData: {
        username: "",
        password: ""
      },
      show1: false,
    }
  },
  methods : {
    clickLogin() {
      this.$axios.post(`/rest-auth/login/`, this.loginData)
      .then (response => {
        window.$cookies.set('auth-token',response.key)
        // this.$router.push({ name: 'Home' })
        // 메인으로 컴포넌트 이동하게 해야함 (emit)
      })
      .catch(err => {
        console.log(err)
        alert('회원 정보가 일치하지 않습니다.')
      })
    },

  },

}
</script>

<style scoped>
  .login-box {
    width: 500px;
    margin: 5rem auto;
  }
  .login-btn {
    margin-top: 2rem;
    float: right;
  }

</style>