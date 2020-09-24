<template>
  <div class="main-wrap">
    <div v-if="!isLogin">여행을 시작할까요?</div>
    <div v-else>
      <h2>{{ username }}님,</h2>
      <h2>제주를 만나보세요!</h2>
    </div>
    <div class="myChoice">
      <button
        class="btn btn-danger"
        @click="clickMyChoice"
      >내가 고르기</button>
    </div>
    <div class="recommend">
      <button
        class="btn btn-danger"
        @click="clickRecommend"
      >식도랑 추천 코스</button>
    </div>
    <ThemePage/>
    <button 
      class="btn btn-primary" 
      @click="clickToLoginPageOrMyPage">{{ loginOrMypage }}</button>
  </div>
</template>

<script>
import ThemePage from '@/components/main/ThemePage.vue'
export default {
    name:'MainPage',
    data() {
        return {
          loginOrMypage: '로그인',
          isLogin: this.$store.state.isLogin,
          username: '',
        }
    },
    mounted() {
      if (this.$store.state.isLogin) {
        const requestHeaders = {
          headers: {
            Authorization: `JWT ${this.$cookies.get("auth-token")}`,
          },
        }
        this.$axios.get(`/rest-auth/user`, requestHeaders)
        .then(res => {
            this.username = res.data.username
        })
        .catch(err => {
            console.error(err)
        })
        this.loginOrMypage = '마이페이지'
      }
    },
    components : {
      ThemePage,
    },
    methods : {
      clickMyChoice() {
        this.$router.push(`/map`)
      },
      clickRecommend() {
        console.log('추천 코스 누름')
      },
      clickToLoginPageOrMyPage() {
        this.$emit('toLoginPageOrMyPage');
      },

    },

}
</script>

<style scoped>
.myChoice, .recommend {
  margin-top: 3rem
}

.main-wrap {
  width: 400px;
	height: 500px;
  margin-left: auto;
	margin-right: auto;
  text-align: center;
}

</style>