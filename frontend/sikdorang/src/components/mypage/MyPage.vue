<template>
	<div>
		<h1>마이페이지</h1>
		<UserProfile/>
		<TripList/>
	</div>
</template>

<script>
import TripList from './TripList.vue'
import UserProfile from './UserProfile.vue'

export default {
	name: "MyPage",
	components: {
		TripList,
		UserProfile,
	},
    mounted() {
		// 유저 정보를 가져옵니다.
		// this.$axios.get()
		this.userInfo = {
			userName: "조규성",
			userBirth: "1995",
			userPhone: "01076338540",
		},
		this.tripItems = [
			[
				{   
					id : 1,
					title: '승희', 
					lat: 36.1406514,
					lng: 128.3271104,
				},
				{   
					id : 2,
					title: '인영', 
					lat: 36.1035992,
					lng: 128.4162945
				},
				{   
					id : 3,
					title: '규성', 
					lat: 36.0954328,
					lng: 128.3963511
				},
				{   
					id : 4,
					title: '성수',
					lat: 36.1115959,
					lng: 128.4303873
				},
				{   
					id : 5,
					title: '도희',
					lat: 36.119735,
					lng: 128.3463003,
				},
				{   
					id : 6,
					title: '마지막',
					lat: 36.119735,
					lng: 118.3463003,
				}
			]
		]
	},
	data() {
		return {
			userInfo: null,
			tripItems: null,
		}
	}
}
</script>

<style>

</style>