<template>
    <div>
        <h2>유저정보</h2>
        <AchievementBadge/>
        <div>{{ getUserInfo.username }}</div>
        <div>{{ 2021 - getUserInfo.age }}세</div>
        <div v-if="getUserInfo.phone_number">{{ getUserInfo.phone_number }}</div>
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