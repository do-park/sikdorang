<template>
  <div class="pay">
    <div class="imp-container">
      <h1>아임포트 결제</h1>
      <button
        class="btn btn-primary"
        @click="handleSubmit">
        결제하기</button>     
    </div>
  </div>
</template>

<script>
// @ is an alias to /src


export default {
  name: 'Payment',
  components: {

  },
  data() {
    return {
      formLayout: 'horizontal',
      form: this.$form.createForm(this, { name: 'payment' }),
      initialMerchantUid: `mid_${new Date().getTime()}`,
      pgs: 'html5_inicis',
      methods: 'card',
      quotas: ['0', '1'],
      initialMethod: 'card',
      vbankDueVisible: false,
      bizNumVisible: false,
      quotaVisible: true,

    }
  },
  methods: {
    handleSubmit(e) {
      e.preventDefault();

      const { IMP } = window;
      IMP.init("imp19424728");
      const data = {
        pg: 'html5_inicis',
        pay_method: 'card',
        escrow: 'checked',
        merchant_uid: this.initialMerchantUid,
        name: '아임포트 VueJS 테스트 결제',
        amount: '1000',
        buyer_name: '홍길동',
        buyer_tel: '01012341234',
        buyer_email: 'example@example.com',
        buyer_addr: '서울시 강남구 신사동 661-16',
        buyer_postcode: '06010',
        niceMobileV2: true,
      };     
      IMP.request_pay(data, this.callback);
    },
   
    callback(response) {
      // result 페이지로 이동
      const query = {
        ...response,
        type: 'payment',
      };
      this.$router.push({ path: '/result', query });
    },
  },
}
</script>

<style scope>

</style>