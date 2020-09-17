<template>
  <div class="login-box">
    <div>로그인 페이지</div>
    <div>
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
    <div>
      <router-link to="/signup">Signup</router-link>
    </div>
    
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
        window.$cookies.set('auth-token',response.data.key)
        this.$store.state.isLogin = true
        this.$emit('clickLogin');
      })
      .catch(err => {
        console.log(err)
        alert('아이디 또는 비밀번호를 다시 확인해주세요.')
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