<template>
    <div>
        <MyPage v-if="isLogin"/>
        <GuideMyPage v-if="isGuide"/>
        <AdminMyPage v-if="isAdmin"/>
    </div>
</template>

<script>
import { mapActions } from 'vuex'
import MyPage from '@/components/mypage/MyPage.vue'
import GuideMyPage from '@/components/mypage/GuideMyPage.vue'
import AdminMyPage from '@/components/mypage/AdminMyPage.vue'


export default {
    name: "MyPageView",
    components: {
        MyPage,
        GuideMyPage,
        AdminMyPage,
    },
    mounted() {
        const requestHeaders = {
            headers: {
                Authorization: `JWT ${this.$cookies.get('auth-token')}`
            }
        }
        this.$axios.get("rest-auth/user/", requestHeaders)
        .then(res => {
            console.log('인증 확인', res)
            this.actionUserInfo(res.data)
            const userCode = res.data.user_code
            if (userCode === 0) {
                this.isLogin = true
            } else if (userCode === 1) {
                this.isLogin = true
                this.isGuide = true
            } else if (userCode === 2) {
                this.isLogin = true
                this.isAdmin = true
            }
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
    data() {
        return {
            isLogin: false,
            isGuide: false,
            isAdmin: false,
        }
    },
}
</script>

<style>

</style>