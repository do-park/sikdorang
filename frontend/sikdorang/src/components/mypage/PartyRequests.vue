<template>
  <div>
    <button class="" data-toggle="modal" :data-target="getPartyId_td">
      <i class="fas fa-comment fa-2x icon-active"></i>
    </button>
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
              <div
                v-for="(request, index) in requestData"
                :key="index"
                class="text-left"
              >
                <b>{{ request.user.username }}</b>
                ({{ request.created_at.split("T")[0] }})
                <div class="mx-3">
                  <viewer
                    v-if="request.content"
                    :initialValue="request.content"
                  />
                </div>
                <hr />
              </div>
            </span>
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
      return `#m${this.partyPk}`;
    },
    getPartyId_id() {
      return `m${this.partyPk}`;
    },
  },
  data() {
    return {
      requestData: [],
    };
  },
  mounted() {
    console.log("partyPK:", this.partyPk);
    this.getPartyRequestData();
  },
  methods: {
    getPartyRequestData() {
      this.$axios
        .get(`/party/list_message/${this.partyPk}`)
        .then((res) => {
          this.requestData = res.data;
          console.log("res", res.data);
          console.log("reqdata", this.requestData);
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>

<style>
.icon-active {
  color: blue;
}
</style>