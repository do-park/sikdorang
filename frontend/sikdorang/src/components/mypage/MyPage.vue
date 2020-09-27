<template>
	<div>
		<h1>마이페이지</h1>
		<hr>
		<UserProfile/>
		<hr>
		<SavedSchedules/>
		<hr>
		<MyPageMap/>
		<hr>
		<TripList/>
		<hr>
		<GuideTourList/>
		<hr>
		<ReviewList/>
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
}
</script>

<style>

</style>