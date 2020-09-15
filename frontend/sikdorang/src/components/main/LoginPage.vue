<template>
  <div class="login-box">
    <div>로그인 페이지</div>
    <v-text-field
      v-model="loginData.email"
      label="이메일"
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
      loginData: {
        email: "",
        password: ""
      },
      show1: false,
    }
  },
  methods : {
    clickLogin() {
      this.$axios.post(`/api/login`, this.loginData)
      .then (response => {
        console.log(response)
      })
      .catch(err => {
        console.log(err)
      })
    }

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