<template>
	<div>
		<div v-if="!isGuide" class="be-guide-wrap">
			<router-link to="#" class="be-guide">가이드 신청</router-link>
		</div>
		<UserProfile/>

		<div class="mt-5">
      <div class="row m-0">
        <button class="col-3 todayBtn mpBtn selected" @click="onTripList">
          <i class="fas fa-bullseye fa-2x"></i>
          <div class="menu-font">오늘의 일정</div>
        </button>
        <button class="col-3 savedSchedulesBtn mpBtn" @click="onSavedSchedules">
          <i class="far fa-calendar-alt fa-2x"></i>
          <div class="menu-font">모든 일정</div>
        </button>
        <button class="col-3 guideTourBtn mpBtn" @click="onGuideTourList">
          <i class="fas fa-suitcase-rolling fa-2x"></i>
          <div class="menu-font">마이 투어</div>
        </button>
        <button class="col-3 reviewBtn mpBtn" @click="onReviewList">
          <i class="fas fa-keyboard fa-2x"></i>
          <div class="menu-font">작성 리뷰</div>
        </button>
      </div>
      <div id="schedule" class="schedule">
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
import ReviewList from '../../views/review/ReviewList'

export default {
	name: "MyPage",
	components: {
		TripList,
		SavedSchedules,
		GuideTourList,
		UserProfile,
		ReviewList,
	},
	props: {
		isGuide: Boolean,
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
  margin-top: 1.5rem;
  min-height: 200px;
}

.mpBtn {
  border: none;
  outline: none !important;
  height: 100%;
  padding: 0px 0px 5px;
}
.menu-icon {
  font-size: 15px;
}
.menu-font {
  font-size: 12px;
}
.selected {
  border-bottom: 3px solid crimson;
}


</style>