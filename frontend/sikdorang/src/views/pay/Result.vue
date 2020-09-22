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
      success: this.getSuccess(query),
      impUid: query.imp_uid,
      merchantUid: query.merchant_uid,
      errorMessage: `${query.error_msg}`,
      buyerName: `${query.buyer_name}`,
      amount: `${query.paid_amount}`,
    };
  },
  methods: {
    getSuccess(query) {
      console.log(query)
      const { success } = query;
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

