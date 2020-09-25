<template>
	<div>
		<h1>마이페이지</h1>
		<UserProfile/>
		<MyPageMap/>
		<TripList/>
		<GuideTourList/>
	</div>
</template>

<script>
import TripList from './TripList.vue'
import GuideTourList from './GuideTourList.vue'
import UserProfile from './UserProfile.vue'
import MyPageMap from './MyPageMap.vue'

export default {
	name: "MyPage",
	components: {
		TripList,
		GuideTourList,
		UserProfile,
		MyPageMap,
	},
}
</script>

<style>

</style>