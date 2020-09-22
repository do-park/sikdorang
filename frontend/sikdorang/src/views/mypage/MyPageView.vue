<template>
    <MyPage/>
</template>

<script>
import { mapActions } from 'vuex'
import MyPage from '@/components/mypage/MyPage.vue'

export default {
    name: "MyPageView",
    components: {
        MyPage,
    },
    mounted() {
        const requestHeaders = {
            headers: {
                Authorization: `JWT ${this.$cookies.get('auth-token')}`
            }
        }
        this.$axios.get("rest-auth/user/", requestHeaders)
        .then(res => {
            console.log(res)
            // this.actionUserInfo(userInfo)
            // this.actionTripList(tripItems)
        })
        .catch(err => console.error(err))
    },
	methods: {
		...mapActions("mypage", [
			'actionUserInfo',
			'actionTripList',
		]),
	},
}
</script>

<style>

</style>