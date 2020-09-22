<template>
  <div class="main-wrap">
    <div>여행을 시작할까요?</div>
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
    <button 
      class="btn btn-primary" 
      @click="clickToLoginPageOrMyPage">btn</button>
      <ThemePage/>
  </div>
</template>

<script>
import ThemePage from '@/components/main/ThemePage.vue'
export default {
    name:'MainPage',
    data() {
        return {

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