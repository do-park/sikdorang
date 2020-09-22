<template>
    <div>
        <MyPage v-if="isUser"/>
        <AchievementBadge/>
        <GuideMyPage v-if="isGuide"/>
        <AdminMyPage v-if="isAdmin"/>
    </div>
</template>

<script>
import { mapActions } from 'vuex'
import MyPage from '@/components/mypage/MyPage.vue'
import AchievementBadge from '@/components/mypage/AchievementBadge.vue'
import GuideMyPage from '@/components/mypage/GuideMyPage.vue'
import AdminMyPage from '@/components/mypage/AdminMyPage.vue'


export default {
    name: "MyPageView",
    components: {
        MyPage,
        AchievementBadge,
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
    data() {
        return {
            isUser: false,
            isGuide: false,
            isAdmin: false,
        }
    },
}
</script>

<style>

</style>