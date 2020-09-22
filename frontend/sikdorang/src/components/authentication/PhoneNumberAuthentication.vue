<template>
    <div>
        <label for="phone_number">휴대폰 번호</label>
        <input type="text" id="phone_number" v-model="number" placeholder="휴대폰 번호 입력(- 제외)">
        <button v-if="!isClicked" @click="onClickAuth()">인증</button>
        <br>
        <input v-if="isClicked" type="text" id="auth_number" v-model="authNumber" placeholder="인증번호 입력">
        <button v-if="isClicked" @click="onClickCheck()">인증</button>
    </div>
</template>

<script>
export default {
    name: "PhoneNumberAuthentication",
    data() {
        return {
            number: null,
            authNumber: null,
            isClicked: false,
        }
    },
    methods: {
        onClickAuth() {
            if (this.number !== null) {
                console.log("핸드폰 인증 절차를 실행합니다.", this.number)
                this.$axios.get(`account/${this.number}/`)
                .then(res => {
                    console.log(res)
                    this.isClicked = true
                })
                .catch(err => console.error(err))
            }
        },
        onClickCheck() {
            // 인증이 완료되면 authenticated를 emit으로 올립니다.
            if (this.authNumber !== null) {
                console.log("인증번호 검증 절차를 실행합니다.", this.authNumber)
                const authData = {
                    phone_num: this.number,
                    auth_num: this.authNumber,
                }
                const requestHeaders = {
                    headers: {
                        Authorization: `JWT ${this.$cookies.get('auth-token')}`
                    }
                }
                console.log(requestHeaders)
                this.$axios.post(`account/phonetoken/`, authData, requestHeaders)
                .then(res => {
                    console.log(res)
                    this.$emit("authenticated")
                })
                .catch(err => console.err(err))
            }
        },
    },
}
</script>

<style>

</style>