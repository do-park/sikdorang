<template>
  <div>
    <div style="height: 5vh"></div>
    <div>
      <h3 class="text-center">[{{ detail.area }}]{{ detail.title }}</h3>
      <div class="date text-center">
        {{ detail.start_date.toString().substr(0, 4) }}년 {{
          detail.start_date.toString().substr(4, 2)
        }}월 {{ detail.start_date.toString().substr(6, 2) }}일 ~
        {{ detail.end_date.toString().substr(0, 4) }}년 {{
          detail.end_date.toString().substr(4, 2)
        }}월{{ detail.end_date.toString().substr(6, 2) }}일
      </div>
      
      <div class="row justify-content-between m-3">
        <div class="col-3 p-0">
          신청 현황
        </div>
        <div class="col-9 p-0 text-right">
          {{ detail.now_person }} / {{ detail.limit_person }}
          <div class="badge badge-secondary" v-if="(detail.now_person < detail.departure_person)">
            {{ detail.departure_person }}명 이상 신청 시 출발
          </div>
          <div class="badge badge-info" v-else>
            출발 가능!
          </div>
        </div>
      </div>
      <div class="row justify-content-between m-3">
        <div class="col-3 p-0">총 금액</div>
        <div class="col-9 p-0 text-right"><span class="price">{{ detail.price }}</span>원</div>
      </div>
      
      <div v-if="isLogin">
        <div v-if="detail.user.username === username" class="row justify-content-between m-3">
          <button class="col-5 p-0 btn btn-outline-secondary">수정하기</button>
          <button class="col-5 p-0 btn btn-outline-danger" @click="deleteTrip">삭제하기</button>
        </div>
        <div v-else-if="isPaied" class="row justify-content-center m-3 y-line">
          <div class="text-center">
            <div>'{{ detail.user.username }}' 가이드와 함께해요.</div>
            <div><span class="strong">{{ detail.start_point }}</span>에서 <span class="strong">{{ detail.start_time }}</span>에 출발합니다.</div>
          </div>
        </div>
        <div v-else-if="!finish" class="row justify-content-center m-3">
          <button class="default-btn" @click="onClick()">
            신청하기
          </button>
        </div>
        <div v-else class="row justify-content-center m-3">
          <div class="y-line">마감되었습니다.</div>
        </div>
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
import Swal from "sweetalert2";
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
        // this.changeDate();
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

    deleteTrip() {
      Swal.fire({
        icon: "warning",
        title: "여행 상품 삭제",
        text: "여행 상품 글을 삭제하시겠습니까?",
        showCancelButton: true,
        confirmButtonText: "삭제합니다.",
        confirmButtonColor: "crimson",
        cancelButtonColor: "gray",
      }).then((result) => {
        if (result.isConfirmed) {
          const requestHeaders = {
            headers: {
              Authorization: `JWT ${this.$cookies.get("auth-token")}`,
            },
          };

          this.$axios
            .delete(`/guide/delete_tour/${this.detail.id}`, requestHeaders)
            .then(() => {
              Swal.fire({
                icon: "success",
                title: "성공적으로 삭제했습니다.",
                confirmButtonColor: "crimson",
              }).then(() => {
                this.$router.push({ name: "TripProductsView" });
              });
            })
            .catch(() => {
              Swal.fire({
                icon: "warning",
                title: "이미 신청한 회원이 있습니다.",
                confirmButtonColor: "crimson",
              });
            });
        }
      });
    },

    login() {
      this.$router.push("/login");
    },
  },
};
</script>

<style scoped>
.img-main {
  display: inline-block;
  width: 100%;
  height: auto;
  background-repeat: no-repeat;
  background-position: center center;
  background-size: cover;
  overflow: hidden;
}
.swal2-popup {
  font-family: "NIXGONM-Vb";
  font-size: 0.7rem !important;
}
.default-btn {
  color: white;
  background-color: crimson;
  padding: 0.5rem 1rem;
  border-radius: 1rem;
}
.date {
  font-size: 13px;
}
.price {
  font-size: 20px;
  color: crimson;
  font-weight: bolder;
}
.strong {
  color: crimson;
  font-weight: bolder;
}
.y-line {
  border-top: 2px solid crimson;
  border-bottom: 2px solid crimson;
  padding: 0.5rem;
}
</style>