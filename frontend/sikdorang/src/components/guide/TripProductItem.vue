<template>
  <div class="row mx-0">
    <img :src="imgSrc" alt="" class="col-3 p-0 img-circle align-self-center" />
    <div class="col-9 p-0">
      <div class="mx-3">
        <div class="m-0 custom-title text-truncate">[{{ item.area }}] {{ item.title.substr(0, 10) }}</div>
        <div>
          <small
            >{{ item.start_date.toString().substr(0, 4) }}년 {{
              item.start_date.toString().substr(4, 2)
            }}월 {{ item.start_date.toString().substr(6, 2) }}일 ~
            {{ item.end_date.toString().substr(0, 4) }}년 {{
              item.end_date.toString().substr(4, 2)
            }}월{{ item.end_date.toString().substr(6, 2) }}일</small
          >
        </div>
        <div>
          {{ item.now_person }} / {{ item.limit_person }}
          <div v-if="ready" class="badge badge-info">
            출발 가능!
          </div>
          <div v-else-if="finish" class="badge badge-danger">
            인원 마감!
          </div>
          <div v-else class="badge badge-secondary">
            {{ item.departure_person }}명 이상 신청 시 출발
          </div>
        </div>
        <div class="text-right mt-2"><span class="price">{{ item.price }}</span> 원</div>
        
        <div class="text-right guide">'{{ item.user.username }}' 가이드 인솔 상품입니다</div>
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

<style scoped>
.img-circle {
  display: inline-block;
  width: 80px;
  height: 13vh;
  padding : 0 ;
  border-radius: 50%;
  background-repeat: no-repeat;
  background-position: center center;
  background-size: cover;
  overflow: hidden;
}
.price {
  font-size: 20px;
  color: crimson;
  font-weight: bolder;
}
.guide {
  font-size: 12px;
}
.custom-title {
  font-weight: bolder;
}
</style>