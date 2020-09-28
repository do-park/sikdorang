<template>
  <div>
    <div>
      <label for="title">제목</label>
      <input class="form-control" type="text" id="title" v-model="partyData.title" />
    </div>
    <editor
      ref="toastuiEditor"
      :initialValue="editorText"
      :options="editorOptions"
      height="500px"
      initialEditType="wysiwyg"
      previewStyle="vertical"
    />
    <button class="btn btn-primary" @click="onClick()">생성</button>
  </div>
</template>

<script>
import "codemirror/lib/codemirror.css";
import "@toast-ui/editor/dist/toastui-editor.css";
import { Editor } from "@toast-ui/vue-editor";


export default {
  name: "PartyForm",
  components: {
    editor: Editor,
  },
  data() {
    return {
      tripPk: "",
      partyData: {
        title: null,
        content: null,
        // 기본 데이터 추가

      },
      editorText: "일정에 대한 소개를 해주세요.",
      editorOptions: {
        hideModeSwitch: true,
      },
    };
  },
  methods: {
    onClick() {
      this.tripPk = window.$cookies.get("party-trip-id")
      this.getHtml();
      const requestHeaders = {
        headers: {
          Authorization: `JWT ${this.$cookies.get("auth-token")}`,
        },
      };
      this.$axios
        .post(`party/create_party/${this.tripPk}`, this.partyData, requestHeaders)
        .then((res) => {
          console.log(res);
          // 등록이 완료되면 상세페이지로 이동
          // this.$router.push(`주소`);
        })
        .catch((err) => console.error(err));
    },
    getHtml() {
      console.log(this.$refs);
      let html = this.$refs.toastuiEditor.invoke("getHtml");
      this.partyData.content = html;
    },
  },
};
</script>

<style>
</style>