<template>
  <div>
    <div>
      <label for="title">제목</label>
      <input class="form-control" type="text" id="title" v-model="tripSchedule.title" />
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
      tripSchedule: {
        title: null,
        content: null,

      },
      editorText: "여행 일정에 대한 자세한 설명을 추가해주세요.",
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
        if (
          this.tripSchedule.title_img === null ||
          this.tripSchedule.title_img === undefined
        ) {
          this.tripSchedule.title_img = "";
        }
      console.log(this.tripSchedule);

      this.$axios
        .post("guide/create_tour", this.tripSchedule, requestHeaders)
        .then((res) => {
          console.log(res);
          // 등록이 완료되면 리턴되는 객체에서 id 값을 이용해 push한다.
          this.$router.push(`/trip/detail/${res.data.id}`);
        })
        .catch((err) => console.error(err));
    },
    getHtml() {
      console.log(this.$refs);
      let html = this.$refs.toastuiEditor.invoke("getHtml");
      this.tripSchedule.content = html;
    },
    fileChange() {
      console.log("!!", this.$refs)
      this.tripSchedule.title_img = this.$refs.tI.files[0];
    },
  },
};
</script>

<style>
</style>