<template>
  <div class="signup">
    <div class="signup-box">
      <v-text-field
        v-model="signupData.email"
        label="이메일"
        :rules="emailRules"
        hide-details="auto"></v-text-field>
      <!-- <v-text-field
        v-model="signupData.phone"
        label="휴대폰 번호"
        :rules="phoneRules"
        type="number"
        hide-details="auto"></v-text-field> -->
      <v-text-field
        v-model="signupData.username"
        label="닉네임"
        :rules="usernameRules"
        hide-details="auto"></v-text-field>
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
        email: "",
        // phone: "",
        username: "",
        year: 1990,
        password1: "",
        password2: "",

      },
      emailRules: [
        value => (value && value.includes('@') && value.includes('.')) || '올바른 이메일을 입력하세요.',
      ],
      // phoneRules: [
      //   value => (value && value.length === 11) || '올바른 휴대폰 번호를 입력하세요.',
      // ],
      usernameRules: [
        value => (value && value.length >= 1) || '1자 이상 입력하세요.',
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
    clickSignup() {
      var pass = false
      if (this.signupData.email.includes('@') && this.signupData.email.includes('.')) {
        // if (this.signupData.phone.length === 11) {
          if (this.signupData.username.length >= 1) {
            if (this.signupData.password1.length >= 8) {
              if (this.signupData.password1 === this.signupData.password2) {
                pass = true
              }
            }
          }
        // } 
      }

      if (pass) {
        console.log(this.signupData)
        this.$axios.post(`/rest-auth/signup/`, this.signupData)
        .then (response => {
          console.log(response)
        })
        .catch(err => {
          console.log(err)
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
