<template>
  <div class="row m-0">
    {{ item }}
    <div class="box">
      <img :src="imgSrc" alt="" class="col-2 p-0 main-img" />
    </div>
    <div class="col-10 p-0">
      <div class="mx-3">
        <h5 class="m-0">[{{ item.area }}] {{ item.title }}</h5>
        <div>
          <small
            >{{ item.start_date.toString().substr(0, 4) }}년
            {{ item.start_date.toString().substr(4, 2) }}월
            {{ item.start_date.toString().substr(6, 2) }}일 ~
            {{ item.end_date.toString().substr(0, 4) }}년
            {{ item.end_date.toString().substr(4, 2) }}월
            {{ item.end_date.toString().substr(6, 2) }}일</small
          >
        </div>
        <!-- item.user 어떻게 들어오는지 보고 닉네임 넣어주기 -->
        <div class="row">
          <!-- <div class="col-6">가이드: {{ item.user }}</div> -->
          <div class="col-6 text-right">{{ item.price }} 원</div>
        </div>
        <div v-if="finish"><small>인원 마감!</small></div>
        <div v-else class="row">
          <div class="col-3">
            {{ item.now_person }} / {{ item.limit_person }}
          </div>
          <div v-if="ready" class="col-9 text-right">
            <small>즉시 출발!</small>
          </div>
          <div v-else class="col-9 text-right">
            <small>최소인원({{ item.departure_person }}) 달성 시 출발</small>
          </div>
        </div>
      </div>
    </div>
    <hr style="width: 100%" />
  </div>
</template>

<script>
export default {
  name: "TripProductItem",
  props: {
    item: Object,
  },
  data() {
    return {
      finish: this.item.limit_person === this.item.now_person,
      ready: this.item.now_person >= this.item.departure_person,
    };
  },
  computed: {
    imgSrc() {
      return this.$store.state.IMG_SERVER_URL + this.item.title_img;
    },
  },
};
</script>

<style>
.box {
  width: 100px;
  height: 100px;
  border-radius: 70%;
  overflow: hidden;
}
.main-img {
  object-fit: contain;
}
</style>