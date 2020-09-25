<template>
    <div>
        <h2>유저정보</h2>
        <AchievementBadge/>
        <div>{{ getUserInfo.userName }}</div>
        <div>{{ 2021 - getUserInfo.userBirth }}세</div>
        <div>{{ getUserInfo.userPhone }}</div>
    </div>
</template>

<script>
import { mapGetters } from "vuex"
import AchievementBadge from './AchievementBadge'
const mypage = "mypage"

export default {
    name: "userProfile",
    components : {
        AchievementBadge,
    },
    computed: {
        ...mapGetters(mypage, [
            'getUserInfo'
        ])
    }
}
</script>

<style>

</style>