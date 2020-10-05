<template>
  <div>
    <div style="height: 5vh"></div>

    <div class="mx-3">
      <input
        class="form-control mx-0"
        type="text"
        id="title"
        v-model="partyData.title"
        placeholder="[지역] 누구와 가고 싶은지 말해주세요"
      />
    </div>
    <editor
      class="mx-3 my-1"
      ref="toastuiEditor"
      :initialValue="editorText"
      :options="editorOptions"
      height="450px"
      initialEditType="wysiwyg"
      previewStyle="vertical"
    />
    <div class="text-right">
      <button
        v-if="type == 1"
        class="btn btn-danger my-3 mx-3"
        @click="updateParty()"
      >
        수정
      </button>
      <button v-else class="btn btn-danger my-2 mx-3" @click="createParty()">
        생성
      </button>
    </div>
  </div>
</template>

<script>
import "codemirror/lib/codemirror.css";
import "@toast-ui/editor/dist/toastui-editor.css";
import { Editor } from "@toast-ui/vue-editor";
import Swal from "sweetalert2";

export default {
  name: "PartyForm",
  components: {
    editor: Editor,
  },
  data() {
    return {
      type: this.$cookies.get("party-type"),
      tripPk: this.$cookies.get("party-trip-id"),
      partyData: {
        title: null,
        content: null,
        trip_date: this.$cookies.get("party-trip-date"),
        // 기본 데이터 추가
      },
      editorText: "일정에 대한 소개를 해주세요.",
      editorOptions: {
        hideModeSwitch: true,
      },
    };
  },
  mounted() {
    console.log(this.type);
    if (this.type == 1) {
      const party = this.$cookies.get("party");
      console.log(party);
      this.partyData.title = party.title;
      this.partyData.content = party.content;
      this.editorText = this.partyData.content;
    }
    console.log("here", this.type, this.tripPk, this.partyData.trip_date);
  },
  methods: {
    datetoint(date) {
      var y = date.substr(0, 4) * 10000;
      var m = parseInt(date.substr(5, 2)) * 100;
      var d = date.substr(8, 2) * 1;
      return y + m + d;
    },
    createParty() {
      console.log("crate");
      // this.tripPk = window.$cookies.get("party-trip-id");
      // this.partyData.trip_date = window.$cookies.get("party-trip-date");
      this.getHtml();
      console.log(this.partyData);
      const requestHeaders = {
        headers: {
          Authorization: `JWT ${this.$cookies.get("auth-token")}`,
        },
      };
      this.$axios
        .post(
          `party/create_party/${this.tripPk}`,
          this.partyData,
          requestHeaders
        )
        .then(() => {
          Swal.fire({
            icon: "success",
            title: "동행 구하기 글을 등록했습니다.",
            confirmButtonColor: "crimson",
          }).then(() => {
            this.$router.push({ name: "PartyList" });
          });
        })
        .catch((err) => console.error(err));
    },
    updateParty() {
      console.log("update");
      this.getHtml();
      const requestHeaders = {
        headers: {
          Authorization: `JWT ${this.$cookies.get("auth-token")}`,
        },
      };
      this.$axios
        .put(
          `party/update_party/${this.tripPk}`,
          this.partyData,
          requestHeaders
        )
        .then((res) => {
          console.log(res);
          Swal.fire({
            icon: "success",
            title: "동행 구하기 글을 수정했습니다.",
            confirmButtonColor: "crimson",
          }).then(() => {
            this.$router.push({ name: "PartyList" });
          });
        })
        .catch((err) => console.error(err));
    },
    getHtml() {
      console.log(this.$refs);
      let html = this.$refs.toastuiEditor.invoke("getHtml");
      this.partyData.content = html;
      console.log(this.partyData);
    },
  },
};
</script>

<style>
.swal2-popup {
  font-family: "NIXGONM-Vb";
  font-size: 0.7rem !important;
}
</style>