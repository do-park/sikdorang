<template>
  <div>
    <h3 class="title">여행 상품 생성</h3>
    <div class="wrap row m-0">
      <input class="form-input col-10 p-0 px-1" placeholder="상품명" type="text" id="title" v-model="tripSchedule.title" />
      <div class="form-input col-10 p-0 row m-0 mx-auto filebox">
        <input @change="fileChange" type="file" ref="tI" id="t-i" accept=".jpg, .jpeg, .gif" />
        <div class="col-8 p-0" v-if="tripSchedule.title_img">{{tripSchedule.title_img.name}}</div>
        <div class="col-8 p-0" v-else></div>
        <label class="col-4 p-0 m-0" for="t-i">대표이미지</label>
      </div>
      <div class="col-10 mx-auto p-0 mt-3 row justify-content-between">
        <input class="form-input col-6 m-0 px-1" placeholder="여행지역" type="text" id="area" v-model="tripSchedule.area" />
        <input
          placeholder="가격"
          class="form-input col-6 m-0 px-1"
          type="number"
          id="price"
          v-model="tripSchedule.price"
        />
      </div>
      <div class="col-10 mx-auto p-0 row">
        <input class="form-input col-5 date-input" type="date" name="start_date" id="start_date" v-model="tripSchedule.start_date" />
        <div class="col-2 p-0 m-0 my-auto text-center">~</div>
        <input class="form-input col-5 date-input" type="date" name="end_date" id="end_date" v-model="tripSchedule.end_date" />
      </div>
      <div class="col-10 mx-auto p-0 row justify-content-between">
        <input
          placeholder="제한인원"
          class="form-input col-6 m-0 px-1"
          type="number"
          id="limit_person"
          v-model="tripSchedule.limit_person"
        />
        <input
          placeholder="최소 출발인원"
          class="form-input col-6 m-0 px-1"
          type="number"
          id="departure_person"
          v-model="tripSchedule.departure_person"
        />
      </div>
      <div class="col-10 p-0 mx-auto mb-0 row justify-content-between form-input">
        <label for="time" class="pl-1 date-time-title" @click="clickStartTime">출발시간</label>
        <input type="time" name="time" id="time" v-model="tripSchedule.start_time" />
      </div>
      <input placeholder="출발장소" class="col-10 pl-1 form-input" type="text" id="start_point" v-model="tripSchedule.start_point" />
    </div>
    <editor
      class="mt-4"
      ref="toastuiEditor"
      :initialValue="editorText"
      :options="editorOptions"
      height="500px"
      initialEditType="wysiwyg"
      previewStyle="vertical"
    />
    <div class="text-center">
      <button class="create-btn" @click="onClick()">작성완료</button>
    </div>
    
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
    clickStartTime(e) {
      e.target.nextSibling.click()
    },
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
        .then(() => {
          this.$router.push(`/mypage`);
        })
        .catch((err) => console.error(err));
    },
    getHtml() {
      let html = this.$refs.toastuiEditor.invoke("getHtml");
      this.tripSchedule.content = html;
    },
    fileChange() {
      this.tripSchedule.title_img = this.$refs.tI.files[0];
    },
  },
};
</script>

<style scoped>
.title {
  margin: 3rem 0px;
  text-align: center;
}
.wrap {
  margin: 0px 5px 1rem;
}
.form-input {
  border-bottom: 2px solid gray;
  margin: 1rem auto ;
}
.filebox label {
  color: gray;
  cursor: pointer;
  padding: 0.05rem !important;
  border: 1px solid #ebebeb;
  text-align: center;
}
.filebox input[type="file"] { 
  /* 파일필드 숨기기 */
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip:rect(0,0,0,0);
  border: 0;
}
.date-input {
  font-size: 13px;
  padding: 0px;
}
.date-time-title {
  color: gray;
}

.create-btn {
  color: white;
  background-color: crimson;
  margin-top: 2rem;
  padding: 0.5rem 1rem;
  border-radius: 1rem;
}

</style>