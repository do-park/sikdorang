<template>
    <div>
        <!-- <img :src="getOrderTrip.img" alt=""> -->
        <h3>{{ getOrderTrip.title }}</h3>
        <span>{{ startDate }} ~ {{ endDate }}</span>
        <span> 가이드: {{ getOrderTrip.userName }}</span>
        <hr>
        <div>
            <h5>가격: {{ getOrderTrip.price }}원</h5>
        </div>
        <h5>{{ getOrderTrip.start_point }} / {{ getOrderTrip.start_time }}</h5>
        <hr>
        <div>
            <h3>예약자 정보</h3>
            <input @click="onClick()" type="checkbox" id="isSame">
            <label for="isSame">주문자와 같음</label>
        </div>
        <label for="orderName">이름 : </label>
        <input class="form-control" type="text" id="orderName" v-model="userName">
        <br>
        <label for="orderPhone">연락처 : </label>
        <input class="form-control" type="text" id="orderPhone" v-model="userPhone">
        <hr>
        <Payment :orderTrip="getOrderTrip" :userName="userName" :userPhone="userPhone" />
        <button class="btn btn-secondary">취소</button>
    </div>
</template>

<script>
import { mapGetters } from 'vuex'
import Payment from "@/views/pay/Payment.vue"

export default {
    name: "TripProductOrder",
    components: {
        Payment
    },
    computed: {
        ...mapGetters("order", [
            "getOrderTrip"
        ]),
    },
    mounted() {
        const requestHeaders = {
            headers: {
                Authorization: `JWT ${this.$cookies.get("auth-token")}`
            }
        }
        this.$axios.get("rest-auth/user/", requestHeaders)
        .then(res => {
            // user 정보를 userInfo에 우선적으로 저장
            console.log(res)
        })
        .catch(err => console.error(err))
    },
    data() {
        return {
            userName: null,
            userPhone: null,
            userInfo: null,
            startDate: `${this.getOrderTrip.start_date.split('-')[0]}년 ${this.getOrderTrip.start_date.split('-')[1]}월 ${this.getOrderTrip.start_date.split('-')[2]}일`,
            endDate: `${this.getOrderTrip.end_date.split('-')[0]}년 ${this.getOrderTrip.end_date.split('-')[1]}월 ${this.getOrderTrip.end_date.split('-')[2]}일`,
        }
    },
    methods: {
        onClick() {
            console.log(this.getOrderTrip)
            this.userName = this.userInfo.userName
            this.userPhone = this.userInfo.userPhone
        }
    }
}
</script>

<style>

</style>