<template>
  <div>
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
  name: "MessageForm",
  components: {
    editor: Editor,
  },
  data() {
    return {
      partyPk: "1",
      messageData: {
        content: null,
      },
      editorText: "호스트에게 자신을 소개하고 연락처를 전달하세요.",
      editorOptions: {
        hideModeSwitch: true,
      },
    };
  },
  methods: {
    onClick() {
      this.getHtml();
      const requestHeaders = {
        headers: {
          Authorization: `JWT ${this.$cookies.get("auth-token")}`,
        },
      };
      this.$axios
        .post(`/party/create_message/${this.partyPk}`, this.messageData, requestHeaders)
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
      this.messageData.content = html;
    },
  },
};
</script>

<style>
</style>