<template>
    <div>
        <label for="phone_number">휴대폰 번호</label>
        <input type="text" id="phone_number" v-model="number">
        <button @click="onClick()">인증</button>
    </div>
</template>

<script>
export default {
    name: "PhoneNumberAuthentication",
    data() {
        return {
            number: null
        }
    },
    methods: {
        onClick() {
            console.log("핸드폰 인증 절차를 실행합니다.", this.number)
        }
    },
}
</script>

<style>

</style>