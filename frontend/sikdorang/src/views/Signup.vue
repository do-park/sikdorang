<template>
  <div class="signup">
    <div class="signup-box">
      <v-text-field
        v-model="signupData.username"
        label="아이디"
        :rules="usernameRules"
        hide-details="auto"
        @keyup="turnUsernameOkToFalse"></v-text-field>
      <v-btn 
        color="primary" 
        @click="checkUsername">중복확인</v-btn>
      <div v-if="clickedCheckUsername">
        <div v-if="!usernameOk">이미 있는 아이디입니다.</div>
        <div v-else>사용 할 수 있는 아이디입니다.</div>
      </div>
      
      <div class="year">
        <v-slider
          v-model="signupData.year"
          label="출생년도"
          :min=1900
          :max="nowYear"
          thumb-label="always"></v-slider>
      </div>
      <v-text-field
        v-model="signupData.password1"
        label="비밀번호"
        :rules="password1Rules"
        :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
        :type="show1 ? 'text' : 'password'"
        hint="8자 이상"
        counter
        @click:append="show1 = !show1"></v-text-field>
      <v-text-field
        v-model="signupData.password2"
        label="비밀번호 확인"
        :rules="password2Rules"
        :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
        :type="show1 ? 'text' : 'password'"
        counter
        @click:append="show1 = !show1"></v-text-field>
      <v-btn 
        class="signup-btn" 
        color="primary" 
        @click="clickSignup">가입하기</v-btn>
    </div>
  </div>
</template>

<script>

export default {
  name: 'Signup',
  data() {
    return {
      signupData: {
        username: "",
        year: 1990,
        password1: "",
        password2: "",

      },
      usernameOk: false,
      clickedCheckUsername: false,
      usernameRules: [
        value => (value && value.length >= 5) || '5자 이상 입력하세요.',
      ],
      nowYear: new Date().getFullYear(),
      show1: false,
      password1Rules: [
        value => (value && value.length >= 8) || '8자 이상 입력하세요.',
      ],
      password2Rules: [
        value => (value === this.signupData.password1) || '비밀번호가 일치하지 않습니다.',
      ],
    }
  },
  methods: {
    turnUsernameOkToFalse() {
      this.usernameOk = false
      this.clickedCheckUsername = false
    },
    checkUsername() {
      if (this.signupData.username.length >= 5) {
        this.clickedCheckUsername = true
        this.$axios.get(`/trip/chk/${this.signupData.username}`)
        .then (response => {
          console.log(response.data)
          if (response.data === '사용 할 수 있는 아이디입니다.') {
            this.usernameOk = true
          }
        })
        .catch(err => {
          console.log(err)
        })
      }
    },
    clickSignup() {
      var pass = false
      if (this.usernameOk) {
        if (this.signupData.password1.length >= 8) {
          if (this.signupData.password1 === this.signupData.password2) {
            pass = true
          }
        }
      }

      if (pass) {
        console.log(this.signupData)
        this.$axios.post(`/rest-auth/registration/`, this.signupData)
        .then (response => {
          window.$cookies.set('auth-token',response.data.key)
          this.$store.state.isLogin = true
          this.$router.push({ name: 'Home' })
        })
        .catch(err => {
          console.log(err)
          alert("너무 일상적인 비밀번호입니다. 변경해주세요.")
        })
      }
      
    }
  },
}
</script>

<style scoped>
  .signup-box {
    width: 500px;
    margin: 5rem auto;
  }
  .year {
    margin-top: 3rem;
  }
  .signup-btn {
    margin-top: 2rem;
    float: right;
  }
</style>
