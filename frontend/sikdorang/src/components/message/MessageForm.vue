<template>
  <div>
    <button type="button" class="btn btn-primary" data-toggle="modal" data-target="#partyRequestModal">동행신청 테스트 버튼</button>


    <!-- Modal -->
    <div class="modal fade" id="partyRequestModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="exampleModalLabel">동행 신청하기</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">

            <editor
              ref="toastuiEditor"
              :initialValue="editorText"
              :options="editorOptions"
              height="500px"
              initialEditType="wysiwyg"
              previewStyle="vertical"
            />

          </div>
          <div class="modal-footer">
            <button class="btn btn-primary" @click="onClick()">보내기</button>
          </div>
        </div>
      </div>
    </div>

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
      partyPk: "1", // 전단계에서 받아와야함
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