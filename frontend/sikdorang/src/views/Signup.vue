<template>
  <div class="signup">
    <div class="signup-box">
      <v-text-field
        v-model="signupData.email"
        label="이메일"
        :rules="emailRules"
        hide-details="auto"></v-text-field>
      <v-text-field
        v-model="signupData.nickname"
        label="닉네임"
        :rules="nicknameRules"
        hide-details="auto"></v-text-field>
      <div class="year">
        <v-slider
          v-model="year"
          label="출생년도"
          :min=1900
          :max="nowYear"
          thumb-label="always"></v-slider>
      </div>
      <v-text-field
        v-model="signupData.password"
        label="비밀번호"
        :rules="[passwordRules.required, passwordRules.min]"
        :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
        :type="show1 ? 'text' : 'password'"
        hint="8자 이상"
        counter
        @click:append="show1 = !show1"></v-text-field>
      <v-text-field
        v-model="signupData.rePassword"
        label="비밀번호 확인"
        :rules="rePasswordRules"
        :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
        :type="show1 ? 'text' : 'password'"
        counter
        @click:append="show1 = !show1"></v-text-field>
      <v-btn class="signup-btn" color="primary">가입하기</v-btn>
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
        nickname: "",
        year: "",
        password: "",
        rePassword: "",

      },
      emailRules: [
        value => (value && value.length >= 5) || '올바른 이메일을 입력하세요.',
      ],
      nicknameRules: [
        value => (value && value.length >= 1) || '1자 이상 입력하세요.',
      ],
      nowYear: new Date().getFullYear(),
      show1: false,
      password: 'Password',
      passwordRules: [
        value => (value && value.length >= 8) || '8자 이상 입력하세요.',
      ],
      rePasswordRules: [
        value => (value === this.signupData.password) || '비밀번호가 일치하지 않습니다.'
      ]
    }
  },
}
</script>

<style>
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
