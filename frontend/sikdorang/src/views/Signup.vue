<template>
  <div class="p-2 signup-wrap">
    <h3 class="my-4 text-center">회원가입</h3>
    <div class="row m-0">
      <input
        type="text"
        class="signup-input col-9"
        v-model="signupData.username"
        placeholder="아이디"
        @keyup="turnUsernameOkToFalse"
      />
      <button class="btn btn-secondary col-3 check-btn" @click="checkUsername">
        중복확인
      </button>
      <div v-if="clickedCheckUsername" class="col-12 p-0">
        <div v-if="!usernameOk">
          <small class="pl-1">{{ errorMsg }}</small>
        </div>
        <div v-else>
          <small class="pl-1">사용 할 수 있는 아이디입니다.</small>
        </div>
      </div>
      <div v-else>
        <div><small class="pl-1">5자 이상 입력하세요</small></div>
      </div>

      <div class="col-12 row p-0 m-0 my-3">
        <label class="col-12 p-0" for="birthYear">나이</label>
        <select id="birthYear" class="custom-select" v-model="signupData.age">
          <option value="2006">10대</option>
          <option value="1996" selected>20대</option>
          <option value="1986">30대</option>
          <option value="1976">40대</option>
          <option value="1966">50대</option>
          <option value="1956">60대</option>
          <option value="1946">70대</option>
        </select>
      </div>
      <div class="col-12 mx-auto p-0 mb-2">
        <input
          type="password"
          class="password-input signup-input col-12"
          v-model="signupData.password1"
          placeholder="비밀번호"
        />
        <small class="pl-1">8자 이상</small>
      </div>

      <div class="col-12 mx-auto p-0">
        <input
          type="password"
          class="password-input signup-input col-12"
          v-model="signupData.password2"
          placeholder="비밀번호 확인"
        />
      </div>

      <div class="col-12 p-0 text-center">
        <button class="col-6 signup-btn" @click="clickSignup">가입하기</button>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions } from "vuex";

export default {
  name: "Signup",
  data() {
    return {
      signupData: {
        username: "",
        age: 1996,
        password1: "",
        password2: "",
      },
      usernameOk: false,
      clickedCheckUsername: false,
      password2Ok: false,
      token: "",
      nowYear: new Date().getFullYear(),
      errorMsg: null,
    };
  },
  methods: {
    ...mapActions("mypage", ["actionUserInfo"]),
    turnUsernameOkToFalse() {
      this.usernameOk = false;
      this.clickedCheckUsername = false;
    },
    checkUsername() {
      if (this.signupData.username.length >= 5) {
        this.clickedCheckUsername = true;
        this.$axios
          .get(`/trip/chk/${this.signupData.username}`)
          .then((response) => {
            // console.log(response.data);
            this.errorMsg = response.data;
            if (response.data === "사용 할 수 있는 아이디입니다.") {
              this.usernameOk = true;
            }
          })
          .catch((err) => {
            console.log(err);
            this.errorMsg = "아이디를 다시 확인해주세요.";
          });
      }
    },
    clickSignup() {
      var pass = false;
      if (this.usernameOk) {
        if (this.signupData.password1.length >= 8) {
          if (this.signupData.password1 === this.signupData.password2) {
            pass = true;
          } else {
            alert("비밀번호가 일치하지 않습니다.");
          }
        } else {
          alert("비밀번호를 8자 이상 설정해주세요.");
        }
      } else {
        alert("아이디를 확인해주세요.");
      }

      if (pass) {
        this.$axios
          .post(`/rest-auth/registration/`, this.signupData)
          .then((response) => {
            window.$cookies.set("auth-token", response.data.token);
            this.$store.state.isLogin = true;
            this.pushUserAge();
          })
          .catch((err) => {
            console.log(err);
            alert("너무 일상적인 비밀번호입니다. 변경해주세요.");
          });
      }
    },
    pushUserAge() {
      const requestHeaders = {
        headers: {
          Authorization: `JWT ${this.$cookies.get("auth-token")}`,
        },
      };
      this.$axios
        .put(`/rest-auth/user/`, this.signupData, requestHeaders)
        .then((response) => {
          response.data.profile_image = this.$store.state.IMG_SERVER_URL + response.data.profile_image.slice(21,-0)
          this.actionUserInfo(response.data);
          this.$router.push("/idealtagcup");
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>

<style scoped>
.signup-wrap {
  border: 5px solid crimson;
  border-radius: 1rem;
  margin: 5rem 1rem;
}
.signup-input {
  display: block;
  border-bottom: 2px solid gray;
}
.check-btn {
  font-size: 14px;
  padding: 0px;
}
.age {
  margin-top: 3rem;
}
.signup-btn {
  margin: 2rem 0px 1rem;
  padding: 0.5rem;
  background-color: crimson;
  color: white;
  border-radius: 1rem;
}
.password-input {
  font-family: "Courier New", Courier, monospace;
}
</style>
