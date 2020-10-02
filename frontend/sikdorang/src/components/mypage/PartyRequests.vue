<template>
  <div>
    <!-- <div v-for="(request, index) in requestData" :key="index">
      <div>보낸사람:</div>
      <div>수신날짜: {{ request.created_at }}</div>
      <div>
        내용:
        <viewer v-if="request.content" :initialValue="request.content" />
      </div>
      <hr />
    </div> -->
    <button
      class="btn btn-primary"
      data-toggle="modal"
      :data-target="getPartyId_td"
    >
      동행 신청자 보기
    </button>
    <hr />
    <!-- Modal -->
    <div
      class="modal fade"
      :id="getPartyId_id"
      tabindex="-1"
      aria-labelledby="exampleModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="exampleModalLabel">동행 신청 현황</h5>
            <button
              type="button"
              class="close"
              data-dismiss="modal"
              aria-label="Close"
            >
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <span v-if="requestData">
              <div v-for="(request, index) in requestData" :key="index">
                <div>보낸사람: {{ request.user.username }}</div>
                <div>수신날짜: {{ request.created_at }}</div>
                <div>
                  내용:
                  <viewer
                    v-if="request.content"
                    :initialValue="request.content"
                  />
                </div>
                <hr />
              </div>
            </span>
            <hr />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import "@toast-ui/editor/dist/toastui-editor-viewer.css";
import { Viewer } from "@toast-ui/vue-editor";

export default {
  name: "PartyRequests",
  components: {
    viewer: Viewer,
  },
  props: {
    partyPk: Number,
  },
  computed: {
    getPartyId_td() {
      console.log(this.partyPk);
      console.log(`#m${this.partyPk}`);
      return `#m${this.partyPk}`;
    },
    getPartyId_id() {
      console.log(this.partyPk);
      console.log(`m${this.partyPk}`);
      return `m${this.partyPk}`;
    },
  },
  data() {
    return {
      requestData: [],
    };
  },
  mounted() {
    this.getPartyRequestData();
  },
  methods: {
    getPartyRequestData() {
      console.log(this.partyPk);
      this.$axios
        .get(`/party/list_message/${this.partyPk}`)
        .then((res) => {
          console.log(res);
          this.requestData = res.data;
          console.log(this.requestData);
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>

<style>
</style>