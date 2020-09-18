<template>
    <div>
        <h2>유저정보</h2>
        <div>{{ getUserInfo.userName }}</div>
        <div>{{ 2021 - getUserInfo.userBirth }}세</div>
        <div>{{ getUserInfo.userPhone }}</div>
    </div>
</template>

<script>
import { mapGetters } from "vuex"

const mypage = "mypage"

export default {
    name: "userProfile",
    computed: {
        ...mapGetters(mypage, [
            'getUserInfo'
        ])
    }
}
</script>

<style>

</style>