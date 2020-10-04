<template>
  <div class="row m-0">
    <img :src="imgSrc" alt="" class="col-3 p-0 img-circle" />
    <div class="col-9 p-0">
      <div class="mx-3">
        <b class="m-0">[{{ item.area }}] {{ item.title.substr(0, 10) }}</b>
        <div>
          <small
            >{{ item.start_date.toString().substr(0, 4) }}-{{
              item.start_date.toString().substr(4, 2)
            }}-{{ item.start_date.toString().substr(6, 2) }} ~
            {{ item.end_date.toString().substr(0, 4) }}-{{
              item.end_date.toString().substr(4, 2)
            }}-{{ item.end_date.toString().substr(6, 2) }}</small
          >
        </div>
        <!-- item.user 어떻게 들어오는지 보고 닉네임 넣어주기 -->
        <div class="">{{ item.user.username }}</div>
        <div class="text-right">{{ item.price }} 원</div>
        <div v-if="finish"><small>인원 마감!</small></div>
        <!-- <div v-else class="row">
          <div class="col-4">
            {{ item.now_person }} / {{ item.limit_person }}
          </div>
          <div v-if="ready" class="col-8 text-right">
            <small>즉시 출발!</small>
          </div>
          <div v-else class="col-8 text-right">
            <small>최소인원({{ item.departure_person }}) 달성 시 출발</small>
          </div>
        </div> -->
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
</style>