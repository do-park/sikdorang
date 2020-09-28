<template>
  <div>
    <div v-for="request in requestData" :key="request.party_id">
      <div>보낸사람: </div>
      <div>수신날짜: {{ request.created_at}}</div>
      <div>내용: 
        <viewer v-if="request.content" :initialValue="request.content"/>
      </div>
      <hr>
    </div>
  </div>
</template>

<script>
import '@toast-ui/editor/dist/toastui-editor-viewer.css'
import { Viewer } from '@toast-ui/vue-editor'

export default {
  name: "PartyRequests",
  components: {
    viewer: Viewer,
  },
  props: {
    partyPk: String
  },
  data() {
    return {
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
        console.log('party~~', res.data)
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