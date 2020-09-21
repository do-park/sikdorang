<template>
    <div>
        <img :src="getOrderTrip.img" alt="">
        <h3>{{ getOrderTrip.title }}</h3>
        <span>{{ getOrderTrip.startDate }} ~ {{ getOrderTrip.endDate }}</span>
        <span> 가이드: {{ getOrderTrip.userName }}</span>
        <hr>
        <div>
            <h5>가격:</h5>
            <h5>{{ getOrderTrip.price }}</h5>
        </div>
        <h5>{{ getOrderTrip.start_point }} / {{ getOrderTrip.start_time }}</h5>
        <hr>
        <div>
            <h3>예약자 정보</h3>
            <input @click="onClick()" type="checkbox" id="isSame">
            <label for="isSame">주문자와 같음</label>
        </div>
        <label for="orderName">이름 : </label>
        <input type="text" id="orderName" v-model="userName">
        <br>
        <label for="orderPhone">연락처 : </label>
        <input type="text" id="orderPhone" v-model="userPhone">
        <hr>
        <button>결제하기</button>
        <button>취소</button>
    </div>
</template>

<script>
import { mapGetters } from "vuex"
export default {
    name: "TripProductOrder",
    computed: {
        ...mapGetters("order", [
            "getOrderTrip"
        ])
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
        })
        .catch(err => console.error(err))
    },
    data() {
        return {
            userName: null,
            userPhone: null,
            userInfo: null,
        }
    },
    methods: {
        onClick() {
            this.userName = this.userInfo.userName
            this.userPhone = this.userInfo.userPhone
        }
    }
}
</script>

<style>

</style>