<template>
  <div class="pay">
    <button
      class="btn btn-primary"
      @click="handleSubmit">
      결제하기</button>
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
    }
  },
  props: [
    'userName',
    'userPhone',
    'orderTrip'
  ],
  methods: {
    handleSubmit(e) {
      window.$cookies.set('ordertrip',this.orderTrip.id)
      e.preventDefault();

      const { IMP } = window;
      IMP.init("imp19424728");
      const data = {
        pg: 'html5_inicis',
        pay_method: 'card',
        merchant_uid: `mid_${new Date().getTime()}`,
        name: '식도랑 가이드투어 결제',
        amount: this.orderTrip.price,
        buyer_name: this.userName,
        buyer_tel: this.userPhone,
        buyer_email: 'example@example.com',
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