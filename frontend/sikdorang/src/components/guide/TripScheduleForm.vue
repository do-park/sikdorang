<template>
  <div class="wraper">
    <div class="input-group mb-3">
      <div class="input-group-prepend">
        <span class="input-group-text">투어이름</span>
      </div>
      <input
        type="text"
        class="form-control"
        placeholder="이걸 뭐라고 부르죠?"
        v-model="tripSchedule.title">
    </div>
    <div>
      <div class="input-group mb-3">
        <div class="input-group-prepend">
          <span class="input-group-text" id="inputGroupFileAddon01">대표사진</span>
        </div>
        <div class="custom-file">
          <input
            type="file"
            class="custom-file-input"
            id="inputGroupFile01" 
            aria-describedby="inputGroupFileAddon01"
            @change="fileChange"
            ref="tI">
          <label class="custom-file-label" for="inputGroupFile01">Choose file</label>
        </div>
      </div>
    </div>
    <div class="input-group mb-3">
      <div class="input-group-prepend">
        <span class="input-group-text">여행지역</span>
      </div>
      <input
        type="text"
        class="form-control"
        placeholder="어디로 가시나요?"
        v-model="tripSchedule.area">
    </div>
    <div class="input-group mb-3">
      <div class="input-group-prepend">
        <span class="input-group-text">투어가격</span>
      </div>
      <input
        type="text"
        class="form-control"
        placeholder="얼마에요?"
        v-model="tripSchedule.price">
      <div class="input-group-append">
        <span class="input-group-text">원</span>
      </div>
    </div>
    <div class="input-group mb-3">
      <div class="input-group-prepend">
        <span class="input-group-text">최대인원</span>
      </div>
      <input
        type="text"
        class="form-control"
        placeholder="몇명까지 갈 수 있죠?"
        v-model="tripSchedule.limit_person">
      <div class="input-group-append">
        <span class="input-group-text">명</span>
      </div>
    </div>
    <div class="input-group mb-3">
      <div class="input-group-prepend">
        <span class="input-group-text">최소인원</span>
      </div>
      <input
        type="text"
        class="form-control"
        placeholder="몇명부터 가세요?"
        v-model="tripSchedule.departure_person">
      <div class="input-group-append">
        <span class="input-group-text">명</span>
      </div>
    </div>
    <div class="input-group mb-3">
      <div class="input-group-prepend">
        <span class="input-group-text">출발날짜</span>
      </div>
      <input
        type="date"
        class="form-control"
        v-model="tripSchedule.start_date">
    </div>
    <div class="input-group mb-3">
      <div class="input-group-prepend">
        <span class="input-group-text">도착날짜</span>
      </div>
      <input
        type="date"
        class="form-control"
        v-model="tripSchedule.end_date">
    </div>
    <div class="input-group mb-3">
      <div class="input-group-prepend">
        <span class="input-group-text">출발시간</span>
      </div>
      <input
        type="time"
        class="form-control"
        v-model="tripSchedule.start_time">
    </div>
    <div class="input-group mb-3">
      <div class="input-group-prepend">
        <span class="input-group-text">출발장소</span>
      </div>
      <input
        type="text"
        class="form-control"
        placeholder="어디서 만날까요?"
        v-model="tripSchedule.start_point">
    </div>
    <editor
      ref="toastuiEditor"
      :initialValue="editorText"
      :options="editorOptions"
      height="500px"
      initialEditType="wysiwyg"
      previewStyle="vertical"
    />
    <button type="button" class="btn btn-primary btn-lg btn-block mt-2" @click="onClick()">등록</button>
  </div>
</template>

<script>
import "codemirror/lib/codemirror.css";
import "@toast-ui/editor/dist/toastui-editor.css";

import { Editor } from "@toast-ui/vue-editor";

// const FirstArea = [
//     "서울", "부산", "인천", "대구", "광주", "대전", "울산", "강원", "경기", "경남", "경북", "전남", "전북", "충남", "충북", "제주"
// ]
export default {
  name: "TripScheduleForm",
  components: {
    editor: Editor,
  },
  data() {
    return {
      tripSchedule: {
        title: null,
        title_img: null,
        area: null,
        start_date: null,
        end_date: null,
        price: null,
        start_point: null,
        start_time: null,
        content: null,
        limit_person: null,
        departure_person: null,
      },
      editorText: "여행 일정에 대한 자세한 설명을 추가해주세요.",
      editorOptions: {
        hideModeSwitch: true,
      },
    };
  },
  mounted() {
    window.scrollTo(0, 0)
  },
  methods: {
    datetoint(date) {
      var y = date.substr(0, 4) * 10000;
      var m = parseInt(date.substr(5, 2)) * 100;
      var d = date.substr(8, 2) * 1;
      return y + m + d;
    },
    onClick() {
      this.getHtml();
      const requestHeaders = {
        headers: {
          Authorization: `JWT ${this.$cookies.get("auth-token")}`,
          'Content-Type': 'multipart/form-data',
        },
      };
        if (
          this.tripSchedule.title_img === null ||
          this.tripSchedule.title_img === undefined
        ) {
          this.tripSchedule.title_img = "";
        }
      const fd = new FormData()
      fd.append('title_img', this.tripSchedule.title_img)
      fd.append('title', this.tripSchedule.title)
      fd.append('area', this.tripSchedule.area)
      fd.append('start_date', this.datetoint(this.tripSchedule.start_date))
      fd.append('end_date', this.datetoint(this.tripSchedule.end_date))
      fd.append('price', this.tripSchedule.price)
      fd.append('start_point', this.tripSchedule.start_point)
      fd.append('start_time', this.tripSchedule.start_time)
      fd.append('content', this.tripSchedule.content)
      fd.append('limit_person', this.tripSchedule.limit_person)
      fd.append('departure_person', this.tripSchedule.departure_person)
      this.$axios
        .post("guide/create_tour", fd, requestHeaders)
        .then((res) => {
          console.log(res);
          this.$router.push(`/mypage`);
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

<style scoped>
.wraper {
  margin: 15px;
}
.input-group-text {
  background-color: white !important;
}
</style>