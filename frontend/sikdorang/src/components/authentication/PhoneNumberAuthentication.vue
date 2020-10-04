<template>
    <div class="text-center wrap">   
        <div class="wrap-head">
            <h5>휴대폰 번호 인증이 필요합니다.</h5>
        </div>
        <div class="wrap-2 row">
            <input class="col-9 p-0 input-custom" type="number" id="phone_number" v-model="number" placeholder="휴대폰 번호를 입력하세요.">
            <button class="col-3 p-0 btn-custom" v-if="!isClicked" @click="onClickAuth()">확인</button>
        </div>
        <div class="wrap-2 row">
            <input class="col-9 p-0 input-custom" v-if="isClicked" type="number" id="auth_number" v-model="authNumber" placeholder="인증 번호를 입력하세요.">
            <button class="col-3 p-0 btn-custom" v-if="isClicked" @click="onClickCheck()">인증</button>
        </div>
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
                    if (res.data.message === 'success') {
                        alert('인증 성공!')
                        this.$router.push('/mypage');
                    } else {
                        alert('인증번호가 일치하지 않습니다.')
                    }
                })
                .catch(err => console.err(err))
            }
        },
    },
}
</script>

<style scoped>
.wrap {
    height: 500px;
    margin: 4rem 0px;
}
.wrap-head {
    margin-bottom: 5rem;
}
.wrap-2 {
    margin: 1rem;
}
.input-custom {
    height: 2rem;
    border-bottom: 1px black solid;
    text-align: center;
}
.btn-custom {
    font-size: 14px;
    background-color: salmon;
    border-radius: 3rem;
}
</style>