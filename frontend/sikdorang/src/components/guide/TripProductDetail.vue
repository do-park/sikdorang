<template>
  <div>
    <div style="height: 5vh"></div>

    <div>
      <h3 class="text-center">[{{ detail.area }}]{{ detail.title }}</h3>
      <div class="text-center">
        {{ detail.start_date.toString().substr(0, 4) }}-{{
          detail.start_date.toString().substr(4, 2)
        }}-{{ detail.start_date.toString().substr(6, 2) }} ~
        {{ detail.end_date.toString().substr(0, 4) }}-{{
          detail.end_date.toString().substr(4, 2)
        }}-{{ detail.end_date.toString().substr(6, 2) }}
      </div>
      <div class="row mx-3 p-0 my-3 justify-content-end">
        가이드: {{ detail.user.username }}
      </div>

      <div class="row mx-3">
        <div class="col-6 my-auto p-0">{{ detail.price }}원</div>
        <div
          v-if="detail.user.username !== username && !isPaied"
          class="col-6 p-0 text-right"
        >
          <div v-if="!finish">
            <button v-if="isLogin" class="btn btn-primary" @click="onClick()">
              신청하기
            </button>
            <div v-else>로그인하세요.</div>
          </div>
          <div v-else>마감되었습니다.</div>
        </div>
        <div v-if="isPaied" class="col-6 p-0 text-right">이미 참가중입니다.</div>
      </div>
    </div>
    <div class="row mx-3">
      <div class="col-4 p-0 text-left">
        {{ detail.now_person }} / {{ detail.limit_person }}
      </div>
      <div class="col-8 p-0 my-1 text-right">
        {{ detail.departure_person }}명 이상 신청 시 출발
      </div>
    </div>

    <hr />
    <div class="mx-3">
      <img :src="imgSrc" alt="" class="img-main" />
    </div>
    <viewer v-if="detail.content" :initialValue="detail.content" class="mx-3" />
  </div>
</template>

<script>
import "@toast-ui/editor/dist/toastui-editor-viewer.css";
import { Viewer } from "@toast-ui/vue-editor";
import { mapActions } from "vuex";

export default {
  name: "TripProductDetail",
  components: {
    viewer: Viewer,
  },
  computed: {
    imgSrc() {
      return this.$store.state.IMG_SERVER_URL + this.detail.title_img;
    },
  },
  mounted() {
    const requestHeaders = {
      headers: {
        Authorization: `JWT ${this.$cookies.get("auth-token")}`,
      },
    };
    this.$axios
      .get(`/guide/detail_tour/${this.$route.params.item_pk}`, requestHeaders)
      .then((res) => {
        this.detail = res.data.result;
        this.isPaied = res.data.flag;
        this.changeDate();
      })
      .catch((err) => console.error(err));
  },
  data() {
    return {
      isLogin: this.$store.state.isLogin,
      username: this.$cookies.get("username"),
      startDate: "2020-01-01",
      endDate: "2020-01-02",
      finish: false,
      detail: {},
      isPaied: false,
    };
  },
  methods: {
    ...mapActions("order", ["actionOrderTrip"]),
    changeDate() {
      console.log(this.detail);
      this.startDate = `${this.detail.start_date.split("-")[0]}년 ${
        this.detail.start_date.split("-")[1]
      }월 ${this.detail.start_date.split("-")[2]}일`;
      (this.endDate = `${this.detail.end_date.split("-")[0]}년 ${
        this.detail.end_date.split("-")[1]
      }월 ${this.detail.end_date.split("-")[2]}일`),
        (this.finish = this.detail.limit_person === this.detail.now_person);
    },
    onClick() {
      this.actionOrderTrip(this.detail);
      this.$router.push("/trip/order");
    },
  },
};
</script>

<style>
.img-main {
  display: inline-block;
  width: 100%;
  height: auto;
  background-repeat: no-repeat;
  background-position: center center;
  background-size: cover;
  overflow: hidden;
}
</style>