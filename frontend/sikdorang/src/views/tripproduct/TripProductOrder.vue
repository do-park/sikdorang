<template>
  <div>
    <div style="height: 5vh"></div>
    <div>
      <h3 class="text-center">[{{ getOrderTrip.area }}]{{ getOrderTrip.title }}</h3>
      <div class="date text-center">
        {{ getOrderTrip.start_date.toString().substr(0, 4) }}년 {{
          getOrderTrip.start_date.toString().substr(4, 2)
        }}월 {{ getOrderTrip.start_date.toString().substr(6, 2) }}일 ~
        {{ getOrderTrip.end_date.toString().substr(0, 4) }}년 {{
          getOrderTrip.end_date.toString().substr(4, 2)
        }}월{{ getOrderTrip.end_date.toString().substr(6, 2) }}일
      </div>
      <div class="row justify-content-center m-3 y-line">
        <div class="text-center">
          <div>'{{ getOrderTrip.user.username }}' 가이드와 함께해요.</div>
          <div><span class="strong">{{ getOrderTrip.start_point }}</span>에서 <span class="strong">{{ getOrderTrip.start_time }}</span>에 출발합니다.</div>
        </div>
      </div>
      <div class="row justify-content-between m-3">
        <div class="col-3 p-0">결제 금액</div>
        <div class="col-9 p-0 text-right"><span class="price">{{ getOrderTrip.price }}</span>원</div>
      </div>
      <div style="height: 2rem"></div>
      <div class="m-3 row">
        <h5 class="col-12 p-0">예약자 정보</h5>
        <input
          class="form-input col-12 p-0 px-1"
          type="text"
          id="orderName"
          v-model="userName"
          placeholder="이름 (실명)"
        />
        <input
          class="form-input col-12 p-0 px-1"
          type="text"
          id="orderPhone"
          v-model="userPhone"
          placeholder="휴대폰 번호"
        />
      </div>

      <div class="pay text-center">
        <button class="default-btn" @click="handleSubmit">결제하기</button>
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

<style scoped>
.price {
  font-size: 20px;
  color: crimson;
  font-weight: bolder;
}
.y-line {
  border-top: 2px solid crimson;
  border-bottom: 2px solid crimson;
  padding: 0.5rem;
}
.date {
  font-size: 13px;
}
.strong {
  color: crimson;
  font-weight: bolder;
}
.default-btn {
  color: white;
  background-color: crimson;
  padding: 0.5rem 1rem;
  border-radius: 1rem;
}
.form-input {
  border-bottom: 2px solid gray;
  margin: 1rem auto ;
}
</style>