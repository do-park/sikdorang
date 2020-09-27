<template>
  <div class="login-box">
    <button 
      class="btn btn-primary" 
      @click="clickToMainPage">메인으로</button>
    <div>로그인 페이지</div>
    <div>
      <input
        type="text"
        class="form-control"
        v-model="loginData.username"
        placeholder="아이디"
        hide-details="auto">
      <input
        type="password"
        class="form-control"
        v-model="loginData.password"
        placeholder="비밀번호">
      <button 
        class="btn btn-primary login-btn" 
        @click="clickLogin">로그인</button>
    </div>
    <div>
      <router-link to="/signup">Signup</router-link>
    </div>
    
  </div>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  name:'LoginPage',
  data() {
    return {
      isLogin: this.$store.state.isLogin,
      loginData: {
        username: "",
        password: ""
      },
    }
  },
  methods : {
    ...mapActions('mypage', ['actionUserInfo']),
    clickLogin() {
      this.$axios.post(`/rest-auth/login/`, this.loginData)
      .then (response => {
        console.log(response)
        window.$cookies.set('auth-token',response.data.token)
        this.$store.state.isLogin = true
        this.actionUserInfo(response.data.user)
        this.$emit('toMainPage');
      })
      .catch(err => {
        console.log(err)
        alert('아이디 또는 비밀번호를 다시 확인해주세요.')
      })
    },
    clickToMainPage() {
      this.$emit('toMainPage');
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