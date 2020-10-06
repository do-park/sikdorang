<template>
  <div>
    <!-- <img :src="getOrderTrip.img" alt=""> -->
    <div class="m-4">
      <h3>{{ getOrderTrip.title }}</h3>
      <span>{{ startDate }} ~ {{ endDate }}</span>
      <span> {{ getOrderTrip.guide_user }} 가이드</span>
      <hr />
      <div>
        <h5>가격: {{ getOrderTrip.price }}원</h5>
      </div>
      <p>
        {{ getOrderTrip.start_point }}에서 {{ getOrderTrip.start_time }}분 출발
        여정
      </p>
      <hr />
      <div>
        <h4 class="mb-3">예약자 정보</h4>
        <input @click="onClick()" type="checkbox" id="isSame" />
        <label for="isSame"> 주문자와 같음</label>
      </div>
      <label for="orderName">이름 : </label>
      <input
        class="form-control"
        type="text"
        id="orderName"
        v-model="userName"
      />
      <br />
      <label for="orderPhone">연락처 : </label>
      <input
        class="form-control"
        type="text"
        id="orderPhone"
        v-model="userPhone"
      />
      <hr />
      <!-- <Payment :orderTrip="getOrderTrip" :userName.sync="userName" :userPhone="userPhone" /> -->
      <div class="pay text-right">
        <button class="btn btn-danger" @click="handleSubmit">결제하기</button>
        <!-- <button class="btn btn-secondary">취소</button> -->
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
// import Payment from "@/views/pay/Payment.vue"

export default {
  name: "TripProductOrder",
  components: {
    // Payment
  },
  computed: {
    ...mapGetters("order", ["getOrderTrip"]),
  },
  mounted() {
    const requestHeaders = {
      headers: {
        Authorization: `JWT ${this.$cookies.get("auth-token")}`,
      },
    };
    this.$axios
      .get("rest-auth/user/", requestHeaders)
      .then(() => {
        // user 정보를 userInfo에 우선적으로 저장
      })
      .catch((err) => console.error(err));
  },
  data() {
    return {
      userName: null,
      userPhone: null,
      userInfo: null,
      startDate: `${this.getOrderTrip.start_date.split("-")[0]}년 ${
        this.getOrderTrip.start_date.split("-")[1]
      }월 ${this.getOrderTrip.start_date.split("-")[2]}일`,
      endDate: `${this.getOrderTrip.end_date.split("-")[0]}년 ${
        this.getOrderTrip.end_date.split("-")[1]
      }월 ${this.getOrderTrip.end_date.split("-")[2]}일`,
    };
  },
  methods: {
    handleSubmit(e) {
      window.$cookies.set("ordertrip", this.getOrderTrip.id);
      window.$cookies.set("user-name", this.userName);
      window.$cookies.set("phone-number", this.userPhone);

      e.preventDefault();

      const { IMP } = window;
      IMP.init("imp19424728");
      const data = {
        pg: "html5_inicis",
        pay_method: "card",
        merchant_uid: `mid_${new Date().getTime()}`,
        name: "식도랑 가이드투어 결제",
        amount: this.getOrderTrip.price,
        buyer_name: this.userName,
        buyer_tel: this.userPhone,
        buyer_email: "example@example.com",
        niceMobileV2: true,
      };
      IMP.request_pay(data, this.callback);
    },

    callback(response) {
      // result 페이지로 이동
      const query = {
        ...response,
        type: "payment",
      };
      this.$router.push({ path: "/result", query });
    },
    onClick() {
      this.userName = this.userInfo.userName;
      this.userPhone = this.userInfo.userPhone;
    },
  },
};
</script>

<style>
</style>