<template>
  <div>
    <div>
      <label for="title">제목</label>
      <input
        class="form-control"
        type="text"
        id="title"
        v-model="partyData.title"
        placeholder="[지역]을 입력해 주세요"
      />
    </div>
    <editor
      ref="toastuiEditor"
      :initialValue="editorText"
      :options="editorOptions"
      height="500px"
      initialEditType="wysiwyg"
      previewStyle="vertical"
    />
    <button v-if="type == 1" class="btn btn-primary" @click="updateParty()">
      수정
    </button>
    <button v-else class="btn btn-primary" @click="createParty()">생성</button>
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
      console.log("party", party);
      this.partyData.title = party.title;
      this.partyData.content = party.content;
      this.editorText = this.partyData.content;
      console.log(this.partyData.title, this.partyData.content);
    }
    console.log(this.type, this.tripPk, this.partyData.trip_date);
  },
  methods: {
    createParty() {
      console.log("crate");
      // this.tripPk = window.$cookies.get("party-trip-id");
      // this.partyData.trip_date = window.$cookies.get("party-trip-date");
      this.getHtml();
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
</style>