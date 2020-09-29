<template>
  <div>
    <h1>{{ type === 'payment' ? '결제' : '본인인증' }} {{ success ? '성공' : '실패'}}</h1>
    <div v-if="!success">
      <div>{{ errorMessage }}</div>
    </div>
    <div v-if="success">
      <h3>주문정보</h3>
      <div>주문번호: {{ merchantUid }}</div>
      <div>주문자: {{ buyerName }}</div>
      <div>결제금액: {{ amount }}원</div>
    </div>
    <button class="btn btn-primary" @click="toMypage">마이페이지로 이동</button>
  </div>
</template>

<script>
export default {
  data() {
    const { query } = this.$router.history.current;
    const { type } = query;
    return {
      type,
      tour: window.$cookies.get('ordertrip'), // 투어 pk
      success: this.getSuccess(query),
      impUid: query.imp_uid,
      merchantUid: query.merchant_uid,
      errorMessage: `${query.error_msg}`,
      buyerName: `${query.buyer_name}`,
      amount: `${query.paid_amount}`,
    };
  },
  methods: {
    postData() {
      const tripId = window.$cookies.get('ordertrip')
      const requestHeaders = {
          headers: {
              Authorization: `JWT ${this.$cookies.get("auth-token")}`
          }
      }
      // 아까 받은 유저이름과 폰번호 같이주기
      this.$axios.post(`guide/paid/${tripId}`, requestHeaders)
			.then(res => {
                console.log(res)
			})
			.catch(err => console.error(err))
    },
    getSuccess(query) {
      const { success } = query;
      if (success === 'true') {
        this.postData()
      }
      const impSuccess = query.imp_success;
      if (impSuccess === undefined) {
        if (typeof success === 'string') {
          return success === 'true';
        }
        return success;
      }
      if (typeof impSuccess === 'string') {
        return impSuccess === 'true';
      }
      return impSuccess;
    },
    toMypage() {
      this.$router.push({ name: 'MyPageView' })
    }
  },
};
</script>

