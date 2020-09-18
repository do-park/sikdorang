<template>
  <div class="main-wrap">
    <div>여행을 시작할까요?</div>
    <div class="myChoice">
      <v-btn
        color="red lighten-2"
        dark
        @click="clickMyChoice"
      >내가 고르기</v-btn>
    </div>
    <div class="recommend">
      <v-btn
        color="red lighten-2"
        dark
        @click="clickRecommend"
      >식도랑 추천 코스</v-btn>
    </div>
    <v-btn 
      class="arrow-btn" 
      color="primary" 
      @click="clickToLoginPageOrMyPage">btn</v-btn>
  </div>
</template>

<script>
export default {
    name:'MainPage',
    data() {
        return {

        }
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