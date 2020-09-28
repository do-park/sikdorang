<template>
  <div>
    나에게 동행 요청한 사람들과 메시지
    <div v-for="request in requestData" :key="request.party_id">
      <div>보낸사람: </div>
      <div>수신날짜: {{ request.created_at}}</div>
      <div>내용: {{ request.content }}</div>
    </div>
  </div>
</template>

<script>

export default {
  name: "PartyRequests",
  data() {
    return {
      partyPk: 1, // 가져와야함
      requestData: []
    };
  },
  mounted() {
    this.getPartyRequestData()
  },
  methods: {
    getPartyRequestData() {
      this.$axios
      .get(`/party/list_message/${this.partyPk}`)
      .then((res) => {
        this.requestData = res.data;
      })
      .catch((err) => {
        console.log(err);
      });
    }
  },
};
</script>

<style>
</style>