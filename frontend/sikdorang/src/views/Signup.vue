<template>
  <div class="signup">
    <div class="signup-box">
      <input
        type="text"
        class="form-control"
        v-model="signupData.username"
        placeholder="아이디"
        :rules="usernameRules"
        hide-details="auto"
        @keyup="turnUsernameOkToFalse">
      <button 
        class="btn btn-primary"
        @click="checkUsername">중복확인</button>
      <div v-if="clickedCheckUsername">
        <div v-if="!usernameOk">이미 있는 아이디입니다.</div>
        <div v-else>사용 할 수 있는 아이디입니다.</div>
      </div>
      
      <div class="age">
        <label for="birthYear">출생년도</label>
        <input
          type="range"
          class="form-control-range"
          id="birthYear"
          :min=1900
          :max="nowYear"
          v-model="signupData.age">
        {{signupData.age}}
      </div>
      <input
        type="password"
        class="form-control"
        v-model="signupData.password1"
        placeholder="비밀번호"
        :rules="password1Rules"
        :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
        hint="8자 이상"
        counter
        @click:append="show1 = !show1">
      <input
        type="password"
        class="form-control"
        v-model="signupData.password2"
        placeholder="비밀번호 확인"
        :rules="password2Rules"
        :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
        counter
        @click:append="show1 = !show1">
      <button
        class="btn btn-primary signup-btn"
        @click="clickSignup">가입하기</button>
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
        age: 1990,
        password1: "",
        password2: "",

      },
      usernameOk: false,
      clickedCheckUsername: false,
      token: '',
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
          window.$cookies.set('auth-token',response.data.token)
          this.$store.state.isLogin = true
          this.pushUserAge()
        })
        .catch(err => {
          console.log(err)
          alert("너무 일상적인 비밀번호입니다. 변경해주세요.")
        })

      }
      
    },
    pushUserAge() {
      const requestHeaders = {
        headers: {
          Authorization: `JWT ${this.$cookies.get('auth-token')}`
        }
      }
      console.log(window.$cookies.get('auth-token'))

      this.$axios.put(`/rest-auth/user/`, this.signupData, requestHeaders)
      .then (response => {
        console.log(response)
        this.$router.push({ name: 'Home' })
      })
      .catch(err => {
        console.log(err)
      })
    }
  },
}
</script>

<style scoped>
  .signup-box {
    width: 500px;
    margin: 5rem auto;
  }
  .age {
    margin-top: 3rem;
  }
  .signup-btn {
    margin-top: 2rem;
    float: right;
  }
</style>
