<template>
  <div>
    <hr>
    <div v-if="!isLogin">여행을 시작할까요?</div>
    <div v-else class="text-left">
      <h2>{{ username }}님,</h2>
      <h2>삼겹살을 만나보세요!</h2>
    </div>
    <hr>
    <div class="btn-wrap row m-0 justify-content-around">
      <div class="w-100 col-4">
        <button
          class="btn btn-danger main-btn"
          @click="clickMyChoice">
          <div>내가</div>
          <div>고르기</div>
        </button>
      </div>
      <div class="w-100 col-4">
        <button
          class="btn btn-danger main-btn d-inline-block"
          @click="clickRecommend">
          <div>식도랑</div>
          <div>추천코스</div>  
        </button>
      </div>
    </div>
    <hr>
    <ThemePage/>
    <hr>
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

.main-wrap {
  width: 400px;
	height: 500px;
  margin-left: auto;
	margin-right: auto;
  text-align: center;
}

.main-btn {
  width: 100px;
  height: 100px;
}

</style>