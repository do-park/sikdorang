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
      hereUserPhone: null,
    }
  },
  props: [
    'userName',
    'userPhone',
    'orderTrip'
  ],
  watch: {
    userPhone() {
      console.log('폰번호', this.userPhone)
      this.hereUserPhone = this.userPhone
    },
    userName() {
      
    }
  },

  methods: {
    handleSubmit(e) {
      window.$cookies.set('ordertrip',this.orderTrip.id)
      window.$cookies.set('user-name', this.userName)
      window.$cookies.set('phone-number', this.userPhone)
      console.log('폰번호', this.userPhone)

      e.preventDefault();

      const { IMP } = window;
      IMP.init("imp19424728");
      // const data = {
      //   pg: 'html5_inicis',
      //   pay_method: 'card',
      //   merchant_uid: `mid_${new Date().getTime()}`,
      //   name: '식도랑 가이드투어 결제',
      //   amount: this.orderTrip.price,
      //   buyer_name: this.userName,
      //   buyer_tel: this.userPhone,
      //   buyer_email: 'example@example.com',
      //   niceMobileV2: true,
      // };     
      // IMP.request_pay(data, this.callback);
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