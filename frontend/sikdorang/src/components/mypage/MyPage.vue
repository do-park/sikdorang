<template>
	<div>
		<div v-if="!isGuide" class="be-guide-wrap">
      <router-link to="#" class="be-guide">가이드 신청</router-link>
		</div>
		<UserProfile/>
		<hr>
		<MyPageMap/>

		<div class="">
      <div class="btn-wrap">
        <button class="todayBtn mpBtn selected" @click="onTripList">오늘의 일정</button>
        <button class="savedSchedulesBtn mpBtn" @click="onSavedSchedules">모든 일정</button>
        <button class="guideTourBtn mpBtn" @click="onGuideTourList">가이드 투어</button>
        <button class="reviewBtn mpBtn" @click="onReviewList">작성한 리뷰</button>
      </div>
      <div id="schedule" class="schedule ptBorder">
				<SavedSchedules :savedSchedules="savedSchedules" />
				<TripList :tripList="tripList" />
				<GuideTourList :guideTourList="guideTourList" />
        <ReviewList :reviewList="reviewList" />

      </div>
    </div>
	</div>
</template>

<script>
import TripList from './TripList.vue'
import SavedSchedules from './SavedSchedules.vue'
import GuideTourList from './GuideTourList.vue'
import UserProfile from './UserProfile.vue'
import MyPageMap from './MyPageMap.vue'
import ReviewList from '../../views/review/ReviewList'

export default {
	name: "MyPage",
	components: {
		TripList,
		SavedSchedules,
		GuideTourList,
		UserProfile,
		MyPageMap,
		ReviewList,
	},
	data() {
		return {
			tripList: true,
			savedSchedules: false,
			guideTourList: false,
			reviewList: false,
		}
	},
	methods: {
		removeSelected() {
			var selected = document.getElementsByClassName('selected')[0]
			selected.classList.remove('selected')
		},
		onTripList() {
            this.tripList = true
			this.savedSchedules = false
			this.guideTourList = false
			this.reviewList = false
			this.removeSelected()
			var target = document.getElementsByClassName('todayBtn')[0]
			target.classList.add('selected')
		},
		onSavedSchedules() {
            this.tripList = false
			this.savedSchedules = true
			this.guideTourList = false
			this.reviewList = false
			this.removeSelected()
			var target = document.getElementsByClassName('savedSchedulesBtn')[0]
			target.classList.add('selected')
		},
		onGuideTourList() {
            this.tripList = false
			this.savedSchedules = false
			this.guideTourList = true
			this.reviewList = false
			this.removeSelected()
			var target = document.getElementsByClassName('guideTourBtn')[0]
			target.classList.add('selected')
		},
		onReviewList() {
            this.tripList = false
			this.savedSchedules = false
			this.guideTourList = false
			this.reviewList = true
			this.removeSelected()
			var target = document.getElementsByClassName('reviewBtn')[0]
			target.classList.add('selected')
        },

	},
}
</script>

<style scoped>
.be-guide-wrap {
  text-align: right;
  margin-top: 5px;
  margin-right: 5px;
}
.be-guide {
  color: gray;
  font-size: 14px;
}
.schedule {

    /* min-height: 500px; */
    background-color: rgba(255, 255, 255, 0.7);
    border-radius: 0px 30px 30px 30px;
}

.mpBtn {
	background-color: gray;
    color: white;
    border: none;
    outline: none !important;
    width: 100px;
    height: 50px;
}
.selected {
	background-color: rgba(143, 160, 242, 1);
}
.mpBtn:hover {
    background-color: rgba(143, 160, 242, 0.8);
}

.btn-wrap {
    text-align: left;
}

</style>